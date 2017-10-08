import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Dialog from 'react-bootstrap-dialog'
import AddScheduleFMSReport from './AddScheduleFMSReport'

class ScheduleTab extends Component {
  constructor(props) {
    super(props)
    this.state = {
      matches: [],
      hasFetchedMatches: false
    }
    this.showError = this.showError.bind(this)
    this.updateMatches = this.updateMatches.bind(this)
    this.clearMatches = this.clearMatches.bind(this)
  }

  updateMatches(matches, onSuccess, onError) {
    this.props.makeTrustedRequest(
      `/api/trusted/v1/event/${this.props.selectedEvent}/matches/update`,
      JSON.stringify(matches),
      onSuccess,
      onError
    )
  }

  clearMatches() {
    this.setState({ matches: [], hasFetchedMatches: false })
  }

  showError(errorMessage) {
    this.dialog.showAlert(errorMessage)
  }

  render() {
    return (
      <div className="tab-pane" id="schedule">
        <Dialog ref={(dialog) => (this.dialog = dialog)} />
        <h3>Match Schedule</h3>
        <div className="row">
          <div className="col-sm-6">
            <AddScheduleFMSReport
              selectedEvent={this.props.selectedEvent}
              showErrorMessage={this.showError}
              updateMatches={this.updateMatches}
              clearMatches={this.clearMatches}
            />
          </div>
        </div>
      </div>
    )
  }
}

ScheduleTab.propTypes = {
  selectedEvent: PropTypes.string,
  makeTrustedRequest: PropTypes.func.isRequired,
}

export default ScheduleTab