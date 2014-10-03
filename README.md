heartbeat
=========

Heartbeat is used to send a custom metric to StackDriver for a heartbeat.
It assumes that the code is running on an EC2 instance.

The main use case for heartbeat is a way of monitoring a service when
normal endpoint monitoring is difficult or impossible.  For example, we
have many Jenkins servers running in our environment.  These are all EC2
instances but they are not accessible except from within our internal
CIDR block.  But we would like to be able to monitor these servers
in StackDriver and send alerts if the servers go down.

Heartbeat accomplishes this by pushing a custom metric to StackDriver.
You can set this up as a job on the Jenkins server itself and run it at
whatever interval you feel comfortable with.  We send a heartbeat every
five minutes.  Then, within StackDriver you can create an alert based on
the absense of this heartbeat for a period of time, e.g. 10 minutes.

The name of the StackDriver custom metric is determined by the value
of a tag on the instance itself.  By default, it uses the ``Name`` tag
but you can configure the tag name to use with the ``--tagname`` option
on the ``heartbeat`` command.

You can also pass the API key for StackDriver either as the ``--apikey``
option or by setting the environment variable ``HEARTBEAT_APIKEY``.  The
``heartbeat`` also uses boto to find the tags associated with the instance
so you will need to ensure that boto credentials are available to the script
when running on the Jenkins server, either by environment variables or via
an IAM Role.  The script only needs access to the ``DescribeTags`` command
in EC2.
