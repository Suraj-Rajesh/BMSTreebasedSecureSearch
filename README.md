# Balanced M-way Tree based Secure Search

Dependencies on CentOS: 

1. sudo yum install python34-setuptools

2. sudo easy_install-3.4 pip

3. sudo yum install gcc libffi-devel python-devel openssl-devel python34-devel

4. $ virtualenv env
   $ source env/bin/activate

4. In virtualenv, 
    pip3 install -r requirements.txt

5. Downlaod ntlk data:
    $ python3
    >> import nltk
    >> nltk.download("all")

6. $ python3 -m textblob.download_corpora

If any problems with pycrypto, refer this url for troubleshooting,
   https://techglimpse.com/openstack-installation-errors-solutions/
