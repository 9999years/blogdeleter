import requests
import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import bs4
import argparse
import sys

sess = requests.Session()
logged_in = False
creds = None

def getcreds(name='creds.json'):
    global creds
    if creds == None:
        with open(name) as f:
            creds = json.load(f)
    return creds

def makepayload(form, user_keys={}):
    payload = {}
    for inp in form.find_all('input'):
        if 'name' in inp.attrs:
            if 'value' in inp.attrs:
                val = inp.attrs['value']
            else:
                val = ''
            payload[inp.attrs['name']] = val
    payload.update(user_keys)
    return payload

def post_form(sess, url, form={}, payload={}):
    pg = sess.get(url)
    form = BeautifulSoup(pg.text, 'html.parser').find(**form)
    payload = makepayload(form, payload)
    act = form['action']
    if (not act.startswith('http://')
            and not act.startswith('https://')):
        # relative url
        act = urljoin(pg.url, act)
    return sess.post(act, data=payload)

def login(creds, session, url='https://www.tumblr.com/login'):
    return post_form(session, url, form={'id': 'signup_form'},
        payload={
            'determine_email': creds['email'],
            'user[email]':     creds['email'],
            'user[password]':  creds['password'],
        },
    )

def delete(url, creds, session):
    del_url = f'https://www.tumblr.com/blog/{url}/delete'
    return post_form(session, del_url, form={'id': 'signup_form'},
        payload={
            'email':     creds['email'],
            'password':  creds['password'],
        },
    )

def setup(credfile='creds.json'):
    global sess
    resp = login(getcreds(credfile), sess)
    if resp.ok:
        logged_in = True
    return resp

def easy_delete(url):
    global sess, logged_in
    if not logged_in:
        setup()
    return delete(url, getcreds(), sess)

def main():
    parser = argparse.ArgumentParser(description='Deletes a Tumblr blog')

    parser.add_argument('url', type='str', help='The url of the blog to delete')

    parser.add_argument('-l', '--log-file', type='str', default='result.html',
            help='Filename to print result HTML to if deleting fails. Default: result.html'
            )
    parser.add_argument('-c', '--credential-file', type='str',
        default='creds.json',
        help='Filename of a credential file; Must be a JSON file containing an `email` key and a `password` key. Default: creds.json')

    args = parser.parse_args()

    login = setup(args.credential_file)
    if not login.ok:
        print('login failure!', file=sys.stderr)
        return
    print(f'Deleting {args.url}... ', end='')
    resp = easy_delete(args.url)
    if resp.ok:
        print('success!')
    else:
        with open(args.log_file, 'w') as f:
            f.write(resp.text)
        print(f'error {resp.status_code}! see: {args.log_file}', file=sys.stderr)

if __name__ == '__main__':
    main()
