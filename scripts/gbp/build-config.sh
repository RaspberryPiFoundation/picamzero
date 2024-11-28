# this is the configuration for buildd-pbuilder.

BASEDIRECTORY=/var/cache/pbuilder/pbuildd/
MIRROR=ftp.debian.org
HOOKDIR=/usr/share/doc/pbuilder/examples/pbuildd/hookdir
ROOTCOMMAND=sudo

# the following is one sample:
function waitingroutine () {
    while sleep 1s; do
    	if ps ax | grep "x[l]ock"; then
		# if xlock does exist, break from loop
		break
	fi
    done
}
