# RPMSpec for a HAProxy 1.7+ stable version RPM on CentOS 7

Perform the following on a build box as a non-root user.

## Install Prerequisites for RPM Creation

    sudo yum -y install rpmdevtools pcre-devel gcc make openssl-devel rpm-build
    rpmdev-setuptree

## Build

    rpmbuild -bb ~/rpmbuild/SPECS/haproxy.spec
    
Resulting RPM will be in /opt/rpm-haproxy/rpmbuild/RPMS/

## Credits

Based on the Red Hat 6.4 RPM spec for haproxy 1.4 combined with work done by [@nmilford](https://www.github.com/nmilford) [@resmo](https://www.github.com/resmo) and [@kevholmes](https://www.github.com/kevholmes)
