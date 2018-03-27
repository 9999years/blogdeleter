Quick Python script for deleting a Tumblr blog.

    usage: blogdeleter.py [-h] [-l LOG_FILE] [-c CREDENTIAL_FILE] url
    
    Deletes a Tumblr blog
    
    positional arguments:
      url                   The url of the blog to delete
    
    optional arguments:
      -h, --help            show this help message and exit
      -l LOG_FILE, --log-file LOG_FILE
                            Filename to print result HTML to if deleting fails.
                            Default: result.html
      -c CREDENTIAL_FILE, --credential-file CREDENTIAL_FILE
                            Filename of a credential file; Must be a JSON file
                            containing an `email` key and a `password` key.
                            Default: creds.json

It does need your password. `creds.json` should look like:

    {
        "email": "example@gmail.com",
        "password": "example"
    }

There’s also a script `delete_many.ps1` to delete a bunch of URLs at once from a
file. `blogdeleter.py` needs to log in again for every URL so this is a bad
solution.
