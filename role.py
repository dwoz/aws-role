#!/usr/bin/env python
import datetime
import dateutil.tz
import errno
import io
import os
import pickle
import subprocess
import sys

import boto3

if sys.version_info[0] >= 3:
    import configparser
else:
    import ConfigParser


SESSION_FILE = 'session.pkl'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def check_perms(file, perm='600'):
    try:
        stat = os.stat(file)
    except OSError as exc:
        if exc.errno == errno.ENOENT:
            return
    return '{:o}'.format(stat.st_mode)[-3:] == perm


def get_config(file, section='role'):
    if not check_perms(file):
        raise Exception("Config file must have 600 permisions")
    if sys.version_info[0] >= 3:
        cp = configparser.ConfigParser()
    else:
        cp = ConfigParser.SafeConfigParser()
    with open(file) as fp:
        cp.readfp(fp)
    return dict(cp.items(section))


def read_session(filename=os.path.join(SCRIPT_DIR, SESSION_FILE)):
    if not os.path.exists(filename):
        return
    if not check_perms(filename):
        raise Exception("Session file must have 600 permisions")
    try:
        with io.open(filename, 'rb') as fp:
            return pickle.load(fp)
    except OSError as exc:
        if exc.errno == errno.ENOENT:
            return
        raise


def write_session(session, filename=os.path.join(SCRIPT_DIR, SESSION_FILE)):
    if not os.path.exists(filename):
        with io.open(filename, 'wb') as fp:
            fp.write('')
        os.chmod(filename, int('10600', 8))
    if not check_perms(filename):
        raise Exception("Session file must have 600 permisions")
    with io.open(filename, 'wb') as fp:
        pickle.dump(session, fp)


def output_environ(session):
    tpl = 'AWS_ACCESS_KEY_ID={} AWS_SECRET_ACCESS_KEY={} AWS_SESSION_TOKEN={}'
    envstr = tpl.format(
        session['AccessKeyId'],
        session['SecretAccessKey'],
        session['SessionToken'],
    )
    sys.stdout.write(envstr)
    sys.stdout.flush()


def ensure_session(**kwargs):
    session = read_session()
    now = datetime.datetime.now(dateutil.tz.tzutc())
    if session and session['Expiration'] > now:
        return
    get_session(**kwargs)


def print_session_env():
    session = read_session()
    now = datetime.datetime.now(dateutil.tz.tzutc())
    if session and session['Expiration'] > now:
        output_environ(session)
        sys.exit(0)
    sys.exit(1)


def get_mfa_code(secret=None):
    if secret:
        cmd = ['oathtool', '--totp', '-b']
        cmd.append(secret)
        try:
            return subprocess.check_output(cmd).strip().decode('utf-8')
        except OSError as exc:
            if exc.errno != errno.ENOENT:
                raise
    return input("Enter the MFA code: ").strip()


def get_session(role, mfa_serial, access_key, secret_key, mfa_secret=None):
    sts_client = boto3.client(
        'sts',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    code = get_mfa_code(mfa_secret)
    assumedRoleObject = sts_client.assume_role(
        RoleArn=role,
        DurationSeconds=10800,
        RoleSessionName="RoleSH",
        SerialNumber=mfa_serial,
        TokenCode=code,
    )
    session = assumedRoleObject['Credentials']
    write_session(session)


if __name__ == '__main__':
    if '--ensure-session' in sys.argv:
        conf = get_config(os.path.join(SCRIPT_DIR, 'role.conf'))
        ensure_session(**conf)
    else:
        print_session_env()
