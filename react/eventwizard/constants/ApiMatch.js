import PropTypes from 'prop-types'

const ALLIANCE_SHAPE = PropTypes.shape({
  teams: PropTypes.arrayOf(PropTypes.string).isRequired,
  score: PropTypes.int
})

const MATCH_SHAPE = PropTypes.shape({
  key: PropTypes.string.isRequired,
  comp_level: PropTypes.string.isRequired,
  set_number: PropTypes.int.isRequired,
  match_number: PropTypes.int.isRequired,
  time_string: PropTypes.string,
  alliances_json: PropTypes.shape({
    red: ALLIANCE_SHAPE,
    blue: ALLIANCE_SHAPE
  })
})

export default MATCH_SHAPE
