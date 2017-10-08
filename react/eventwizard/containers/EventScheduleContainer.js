import { connect } from 'react-redux'
import ScheduleTab from '../components/scheduleTab/ScheduleTab'
import makeTrustedApiRequest from '../net/TrustedApiRequest'

const mapStateToProps = (state) => ({
  selectedEvent: state.auth.selectedEvent,
  makeTrustedRequest: (requestPath, requestBody, onSuccess, onError) => {
    makeTrustedApiRequest(state.authId, state.authSecret, requestPath, requestBody, onSuccess, onError)
  },
})

export default connect(mapStateToProps)(ScheduleTab)
