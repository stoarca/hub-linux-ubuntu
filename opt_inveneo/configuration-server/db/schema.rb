# This file is autogenerated. Instead of editing this file, please use the
# migrations feature of ActiveRecord to incrementally modify your database, and
# then regenerate this schema definition.

ActiveRecord::Schema.define(:version => 1) do

  create_table "initial_configs", :force => true do |t|
    t.column "mac",                :string,  :default => "NULL"
    t.column "timezone",           :string,  :default => "NULL"
    t.column "ntp_on",             :boolean, :default => false,  :null => false
    t.column "ntp_servers",        :string,                      :null => false
    t.column "proxy_on",           :boolean, :default => false,  :null => false
    t.column "http_proxy",         :string,  :default => "NULL"
    t.column "http_proxy_port",    :integer, :default => 8080,   :null => false
    t.column "https_proxy",        :string,  :default => "NULL"
    t.column "https_proxy_port",   :integer, :default => 8080,   :null => false
    t.column "ftp_proxy",          :string,  :default => "NULL"
    t.column "ftp_proxy_port",     :integer, :default => 8080,   :null => false
    t.column "phone_home_on",      :boolean, :default => false,  :null => false
    t.column "phone_home_reg",     :string,  :default => "NULL"
    t.column "phone_home_checkin", :string,  :default => "NULL"
    t.column "locale",             :string,                      :null => false
    t.column "single_user_login",  :boolean, :default => false,  :null => false
  end

  create_table "sessions", :force => true do |t|
    t.column "session_id", :string,   :default => "NULL"
    t.column "data",       :text,     :default => "NULL"
    t.column "updated_at", :datetime
  end

  add_index "sessions", ["updated_at"], :name => "index_sessions_on_updated_at"
  add_index "sessions", ["session_id"], :name => "index_sessions_on_session_id"

end
