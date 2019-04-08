# Metro Automation Engine Release Notes
## Release 3.2.1
### Resolved Issues
* Fix static routes so they are applied to VSC (METROAE-953)
* Handle spaces in the yum.conf proxy setting in metro-setup.sh
* Fix nsgv-postdeploy to check proper bootstrap status (METROAE-959)
* Move internal IP fields out of AWS section of VSC schema (METROAE-961)
* Force VSD upgrade ordering (METROAE-966)
* Fix encrypt credentials encoding error (METROAE-963)
