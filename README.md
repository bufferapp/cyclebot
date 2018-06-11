# Cycle Slack Bot

A simple bot that provides information on Buffer cycles.

# Technical details

Implemented as a [Slack App](https://api.slack.com/apps/AAQBGG67L/general?) with a single [`/buffercycles`](https://api.slack.com/apps/AAQBGG67L/slash-commands?) slash command.

Slash command is built using a flask app that's deployed with [slam](https://github.com/miguelgrinberg/slam)

# Development/Deployment

You'll need Python 3.6 and pip.

To run the command locally:

`make run`

To deploy the app (make sure you have aws-cli installed and have the correct IAM credentials configured):

`make deploy`
