import PropTypes from 'prop-types'

const TEAM_SHAPE = PropTypes.shape({
  key: PropTypes.string.isRequired,
  team_number: PropTypes.number.isRequired,
  nickname: PropTypes.string.isRequired
})

export default TEAM_SHAPE
