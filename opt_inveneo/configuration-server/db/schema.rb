# This file is autogenerated. Instead of editing this file, please use the
# migrations feature of ActiveRecord to incrementally modify your database, and
# then regenerate this schema definition.

ActiveRecord::Schema.define(:version => 1) do

  create_table "initial_configs", :force => true do |t|
    t.column "mac",                :string,  :default => "NULL"
    t.column "timezone",           :string,  :default => "'America/Los_Angeles'"
    t.column "hostname",           :string,  :default => "NULL"
    t.column "hostname_prefix",    :string,  :default => "'inveneo-cs-'"
    t.column "ntp_on",             :boolean, :default => false,                                                 :null => false
    t.column "ntp_servers",        :string,  :default => "'pool.ntp.org'",                                      :null => false
    t.column "proxy_on",           :boolean, :default => false,                                                 :null => false
    t.column "http_proxy",         :string,  :default => "'192.168.100.1:8080'"
    t.column "https_proxy",        :string,  :default => "NULL"
    t.column "ftp_proxy",          :string,  :default => "'192.168.100.1:8080'"
    t.column "phone_home_on",      :boolean, :default => false,                                                 :null => false
    t.column "phone_home_reg",     :string,  :default => "'http://community.inveneo.org/phone-home2/register'"
    t.column "phone_home_checkin", :string,  :default => "'http://community.inveneo.org/phone-home2/checkin'"
    t.column "locale",             :string,  :default => "'en_US.utf8'",                                        :null => false
  end

end
