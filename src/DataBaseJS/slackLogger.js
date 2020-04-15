const SlackNotify = require('slack-notify')

const SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

const slack = SlackNotify(SLACK_WEBHOOK_URL)

const logToDebug = slack.extend({
  channel: '#debug',
  username: 'slacker',
  icon_emoji: ':dissapointed:'
})


module.exports = logToDebug
