import React, { Component } from 'react'
import PropTypes from 'prop-types'
import FileInput from 'react-file-input'
import Dialog from 'react-bootstrap-dialog'
import {RadioGroup, Radio} from 'react-radio-group'
import ensureRequestSuccess from '../../net/EnsureRequestSuccess'

class AddScheduleFMSReport extends Component {

  // Table headers start on the 4th row
  HEADER_START_ROW = 4

  constructor(props) {
    super(props)
    this.state = {
      selectedFileName: '',
      message: '',
      stagingMatches: [],
      selectedCompLevel: '',
    }
    this.onFileChange = this.onFileChange.bind(this)
    this.parseFMSReport = this.parseFMSReport.bind(this)
    this.updateCompLevel = this.updateCompLevel.bind(this)
  }

  updateCompLevel(compLevel) {
    this.setState({selectedCompLevel: compLevel})
  }

  onFileChange(event) {
    if (event && event.target && event.target.files.length > 0) {
      const f = event.target.files[0]
      const reader = new FileReader()
      const name = f.name
      reader.onload = this.parseFMSReport
      this.setState({
        selectedFileName: name,
        message: 'Processing file...',
      })
      reader.readAsBinaryString(f)
    } else {
      this.setState({ selectedFileName: '' })
    }
  }

  makeTeamKey(number) {
    return "frc" + number.trim().replace("*", "")
  }

  parseFMSReport(event) {
    const data = event.target.result

    // eslint-disable-next-line no-undef
    const workbook = XLSX.read(data, {type: 'binary'})
    const firstSheet = workbook.SheetNames[0]
    const sheet = workbook.Sheets[firstSheet]

    // parse the excel to array of matches
    // headers start on 2nd row
    // eslint-disable-next-line no-undef
    const matchesInFile = XLSX.utils.sheet_to_json(sheet, {range: this.HEADER_START_ROW})
    const validMatches = matchesInFile.filter(row => row['Match'])
    const fmsMatchNums = validMatches.map(row => parseInt(row['Match'], 10))
    fetch("/_/match-keys/" + this.props.selectedEvent + "/qm", {
      method: 'POST',
      credentials: 'same-origin',
      body: JSON.stringify(fmsMatchNums)
    })
      .then(ensureRequestSuccess)
      .then(response => response.json())
      .then(data =>
        validMatches.map(row => {
          const fmsNum = parseInt(row['Match'])
          const tbaKeyData = data[fmsNum]
          const redAlliance = {
            teams: [
              this.makeTeamKey(row['Red 1']),
              this.makeTeamKey(row['Red 2']),
              this.makeTeamKey(row['Red 3'])
            ],
            score: null
          }
          const blueAlliance = {
            teams: [
              this.makeTeamKey(row['Blue 1']),
              this.makeTeamKey(row['Blue 2']),
              this.makeTeamKey(row['Blue 3'])
            ],
            score: null
          }
          return {
            key: tbaKeyData['key'],
            comp_level: tbaKeyData['comp_level'],
            match_number: tbaKeyData['match_num'],
            set_num: tbaKeyData['set_num'],
            time_string: row['Time'],
            alliances: {
              red: redAlliance,
              blue: blueAlliance
            }
          }
        })
      )
      .then(matches => {
        if (matches.length === 0) {
          this.setState({message: 'No matches found in the file. Try opening the report in Excel and overwriting it using File->Save As'})
          return
        }

        this.setState({
          message: '',
          stagingMatches: matches,
        })
      })
      .then(() => {
        this.reportConfirmDialog.show({
          title: `Confirm Matches: ${this.state.selectedFileName}`,
          body: `${this.state.stagingMatches.length} matches found in report`,
          bsSize: 'large',
          actions: [
            Dialog.CancelAction(),
            Dialog.Action(
              'Confirm',
              () => {
                this.setState({message: 'Uploading matches...'})
                this.props.updateMatches(
                  this.state.stagingMatches,
                  () => {
                    this.setState({
                      selectedFileName: '',
                      message: `${this.state.stagingMatches.length} matches added to ${this.props.selectedEvent}`,
                      stagingMatches: [],
                    })
                    this.props.clearMatches()
                  },
                  (error) => (this.props.showErrorMessage(`${error}`)))
              },
              'btn-primary'
            ),
          ],
        })
      })
      .catch((error) => (this.props.showErrorMessage(`${error}`)))
  }

  render() {
    return (
      <div>
        <h4>Import FMS Report</h4>
        <p>This will <em>append</em> to the existing matches for this event.</p>
        {this.state.message &&
          <p>{this.state.message}</p>
        }
        <h4>Select Match Level</h4>
        <RadioGroup
          name="compLevelImportSelector"
          selectedValue={this.state.selectedCompLevel}
          onChange={this.updateCompLevel}
        >
          <Radio value="qm" />Qual
          <Radio value="ef" />Octofinal
          <Radio value="qf" />Quarterfinal
          <Radio value="sf" />Semifinal
          <Radio value="f" />Final
        </RadioGroup>
        <FileInput
          name="FMSScheduleReport"
          accept=".xlsx"
          placeholder="Click to choose file"
          onChange={this.onFileChange}
          disabled={!this.props.selectedEvent || !this.props.selectedCompLevel}
        />
        <Dialog
          ref={(dialog) => (this.reportConfirmDialog = dialog)}
        />
      </div>
    )
  }
}


AddScheduleFMSReport.propTypes = {
  selectedEvent: PropTypes.string,
  showErrorMessage: PropTypes.func.isRequired,
  updateMatches: PropTypes.func.isRequired,
  clearMatches: PropTypes.func,
}

export default AddScheduleFMSReport