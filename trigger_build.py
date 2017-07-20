#!/usr/bin/env python

import argparse
import urllib2

servers = ["eng-scmsrv-02", "eng-scmsrv-01"]

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('rpmname')
    parser.add_argument('rpmver')
    return parser.parse_args()

def trigger_single_build(namever, server_url):
    url = 'http://{}.morphodetection.com:8080/job/{}/build?token={}'

    rq = urllib2.Request(url.format(server_url, namever, namever))
    try:
        response = urllib2.urlopen(rq).read()
        print "{}: {}".format(namever, response)
    except urllib2.URLError as e:
        print "{}: {}".format(namever, e)
        return False
    return True

def trigger_build(namever):
    for server in servers:
        if trigger_single_build(namever, server):
            return True
    print "Unable to trigger build on {}".format(",".join(servers))
    return False

def main(args):
    jname = "-".join([args.rpmname, args.rpmver, "build-setup"])
    # Try each server, starting from the newest.
    # Return if you didn't get a URLError
    if trigger_build(jname):
        return 0
    else:
        return 1

if __name__ == "__main__":
    main(get_args())

