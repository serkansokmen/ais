# now_build_staticfiles.sh

# Install Python 3.6 since it is missing in the Now build environment
yum install -y https://centos6.iuscommunity.org/ius-release.rpm
yum install -y python36u

# Install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.6 get-pip.py

# Install project requirements
pip install -r requirements.txt

# Build staticfiles
python3.6 manage.py collectstatic
python3.6 manage.py djstripe_init_customers 
python3.6 manage.py djstripe_sync_plans_from_stripe

mkdir -p media
mkdir -p media/uploads

