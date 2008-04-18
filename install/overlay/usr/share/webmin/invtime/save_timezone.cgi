#!/usr/bin/perl
# Update the timezone

require '../time/time-lib.pl';
require '../time/linux-lib.pl';

&ReadParse();
$access{'timezone'} || &error($text{'timezone_ecannot'});

&error_setup($text{'timezone_err'});
$in{'zone'} || &error($text{'timezone_enone'});
&set_current_timezone($in{'zone'});
&restart_miniserv();
&webmin_log("timezone", undef, $in{'zone'});
&redirect("");

