#!/usr/bin/perl
# Either redirects to link.cgi, if a URL has been set, or asks for a URL
require './invshare-lib.pl';
use form;
use share;
&ReadParse();

$msg = $in{'msg'};

if ($config{'url'}) {
	&redirect("link.cgi/$config{'url'}");
} else {
	&ui_print_header(undef, $module_info{'desc'}, "", undef, 1, 1);     

	if ( $msg ) {
		print "<h4>" . un_urlize($msg) . "</h4><br>";
	}
	

	@sharetable= ("Share Name", "Owner", "Delete");
	print "<h2>Network Shares</h2>\n";
	print &ui_columns_start(\@sharetable);


        @shares = get_share_names(SHARE_CONF_DIR);  
        foreach $share (@shares) {
			$column1 = $share; 
                        $column2 = get_share_owner($share);
			$column3 = "<a href='delshare.cgi?sharename=" . urlize($share) . "'>Delete</a>";
			@sharetablerow= ($column1, $column2, $column3);
			print &ui_columns_row(\@sharetablerow);
	}
	print &ui_columns_end();
	print "<br>\n";
	print "<h2>Add a new network share</h2>\n";
	print &ui_form_start("createshare.cgi");
	print "<table>";
        input_box_row("sharename","Share Name");

        $users_list = get_users_list();
        @sel_list = ();
	push @sel_list, [ "- Public Share -", "- Public Share -" ];
        foreach $user ( @{ $users_list } ) {
                push @sel_list, [ @{ $user }[1], @{ $user }[1] ];
        }

        print_row_title("Owner",&ui_select("owner", "", \@sel_list));
	print "<tr><td valign='top'>",&ui_submit("Create"),"</td></tr></table>\n";
	print &ui_form_end();
	&ui_print_footer("/", $text{'index'});
}

