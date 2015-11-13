heartbeat
=========

Heartbeat is used to send a custom metric to Datadog for a heartbeat. It assumes
that the code is running on an EC2 instance.

The main use case for heartbeat is a way of monitoring a service when normal
endpoint monitoring is difficult or impossible.  For example, we have many
Jenkins servers running in our environment.  These are all EC2 instances but
they are not accessible except from within our internal CIDR block.  But we
would like to be able to monitor these servers in Datadog and send alerts if the
servers go down.

Heartbeat accomplishes this by pushing a custom metric to Datadog. You can set
this up as a job on the Jenkins server itself and run it at whatever interval
you feel comfortable with.  We send a heartbeat every five minutes.  Then,
within Datadog you can create an alert based on the absence of this heartbeat
for a period of time, e.g. 10 minutes.

The name of the Datadog custom metric is determined by the value of a tag on the
instance itself.  By default, it uses the ``Name`` tag but you can configure the
tag name to use with the ``--tagname`` option on the ``heartbeat`` command.

You can also pass the API key for Datadog either as the ``--apikey`` option or
by setting the environment variable ``HEARTBEAT_APIKEY``. It also requires an
app key, specified with ``--appkey`` or the environment variable
``HEARTBEAT_APPKEY``.

The ``heartbeat`` also uses boto to find the tags associated with the instance
so you will need to ensure that boto credentials are available to the script
when running on the Jenkins server, either by environment variables or via an
IAM Role.  The script only needs access to the ``DescribeTags`` command in EC2.

Jenkins Configuration
---------------------

There are probably lots of ways you could use heartbeat but the way we
use it is to install it as a job on our Jenkins servers and schedule the job
to run every 5 minutes or so.

The actual command we run in Jenkins looks like this:

    PYENV_HOME=$WORKSPACE/.pyenv/

    # Delete previously built virtualenv
    if [ -d $PYENV_HOME ]; then
        rm -rf $PYENV_HOME
    fi

    # Create virtualenv and install necessary packages
    virtualenv --no-site-packages $PYENV_HOME
    . $PYENV_HOME/bin/activate
    pip install --quiet nosexcover
    pip install --quiet pylint
    pip install -r $WORKSPACE/requirements.txt
    pip install --quiet $WORKSPACE/  # where your setup.py lives
    $WORKSPACE/bin/heartbeat --debug --tagname Name

This instructs heartbeat to use the value of the ``Name`` tag on the
instance to construct the name of the custom metric written to Datadog.
This also writes debug output the console output to help find any issues
in getting the configuration sorted out.
