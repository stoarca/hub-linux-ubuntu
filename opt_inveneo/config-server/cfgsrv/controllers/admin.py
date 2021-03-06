import logging
import cgi
import os
import shutil

from cfgsrv.lib.base import *
from cfgsrv.controllers.authentication import *

log = logging.getLogger(__name__)

class AdminController(AuthenticationController):

    ###########################
    # controller methods
    ###########################    
    def index(self):
        """simply redirect to dashboard"""
        log.debug('index()')
        return redirect_to('/admin/dashboard')

    def dashboard(self):
        """render the dashboard"""
        log.debug('dashboard()')
        servers = model.Session.query(model.Server)
        c.Server = servers.filter(model.Server.name == g.DEFAULT_SERVER).one()
        return render('/dashboard.mako')

    def toggle_server(self):
        """switch server ON or OFF (no param is toggle)"""
        name = request.params.get('name', g.DEFAULT_SERVER)
        log.debug('toggle_server(%s)' % name)
        servers = model.Session.query(model.Server)
        server = servers.filter(model.Server.name == name).one()
        server.server_on = not server.server_on
        model.Session.update(server)
        model.Session.commit()
        redirect_to('/admin/dashboard')

    def display_station(self):
        """redirect to mako page rendition"""
        stations = model.Session.query(model.Station)
        c.Station = stations.filter(model.Station.mac == g.DEFAULT_MAC).one()
        return render('/edit_station.mako')

    def edit_station(self):
        """edit the settings of a station, or create a new one"""
        mac = request.params.get('mac', g.DEFAULT_MAC)
        log.debug('edit_station(%s)' % mac)

        # collect desired request params into dictionary
        # XXX need to do form validation here
        items = request.params

        stations = model.Session.query(model.Station)
        station = stations.filter(model.Station.mac == mac).first()
        if not station:
            station = model.Station(mac)
            model.Session.save(station)
        station.update(items)
        model.Session.update(station)
        model.Session.commit()
        redirect_to('/admin/dashboard')

    def reset_stations(self):
        """reset all stations to the default configuration"""
        # XXX currently everyone shares the default MAC
        mac = g.DEFAULT_MAC
        stations = model.Session.query(model.Station)
        station = stations.filter(model.Station.mac == mac).one()
        station.clone(model.Station())
        model.Session.update(station)
        model.Session.commit()

        # reset all config archives
        for type in ['station', 'user']:
            path = h.get_config_dir_for(type)
            src = os.path.join(path, '..', g.FACTORY_CONFIG)
            for f in os.listdir(path):
                if f.endswith('.tar.gz'):
                    dst = os.path.join(path, f)
                    log.debug('%s -> %s' % (src, dst))
                    shutil.copyfile(src, dst)

        redirect_to('/admin/dashboard')

    """
    # MORE CRUFT

    def config_remove(self, id):
        mac = str(id)

        if mac == NONE:
            log.error('Need a valid unique mac identifier')
            abort(400)

        try:
            q = model.Session.query(model.Config).filter(model.Config.mac == mac).one()
            model.Session.delete(q)
            model.Session.commit()
        except:
            abort(400)

        redirect_to('/admin/list_initial_configurations')

    def config_add(self):
        c.Config = model.Config()
        c.Edit = False
        return render('/config_edit.mako')

    def config_edit_process(self, id):
        log.debug('config edit process for: ' + str(id))
        newconfig_q = self._get_config_entry_by_id_or_mac_or_create(id)
        is_edit = False

        try:
            newconfig_q.mac = cgi.escape(request.POST['mac'])
        except:
            is_edit = True
        newconfig_q.lang = cgi.escape(request.POST['lang']) 
        newconfig_q.time_zone = cgi.escape(request.POST['time_zone'])

        newconfig_q.config_host = cgi.escape(request.POST['config_host']) 
        newconfig_q.config_host_type = \
                cgi.escape(request.POST['config_host_type']) 

        newconfig_q.proxy_on = h.is_checkbox_set(request, 'proxy_on', log)
        newconfig_q.ntp_on = h.is_checkbox_set(request, 'ntp_on', log)
        newconfig_q.ntp_servers = cgi.escape(request.POST['ntp_servers']) 

        newconfig_q.hub_docs_dirs_on = \
                h.is_checkbox_set(request, 'hub_docs_dirs_on', log)
        newconfig_q.local_shared_docs_dir_on = \
                h.is_checkbox_set(request, 'local_shared_docs_dir_on', log)
        newconfig_q.local_user_docs_dir_on = \
                h.is_checkbox_set(request, 'local_user_docs_dir_on', log)

        newconfig_q.phone_home_on = \
                h.is_checkbox_set(request, 'phone_home_on', log)
        newconfig_q.phone_home_reg_url = \
                cgi.escape(request.POST['phone_home_reg_url']) 
        newconfig_q.phone_home_checkin_url = \
                cgi.escape(request.POST['phone_home_checkin_url']) 

        error = self._validate_configuration(newconfig_q, is_edit)

        if len(error) == 0:
            log.debug('found error in one of the values')
            model.Session.save(newconfig_q)
            model.Session.commit()
        else:
            c.Error = error
            c.Edit = is_edit
            c.Config = newconfig_q
            return render('/config_edit.mako')

        c.Config = None

        redirect_to('/admin/config_edit_done')

    def config_edit_done(self):
        redirect_to('/admin/list_initial_configurations')
        
    def station_remove(self, id):
        mac = str(id)

        if mac == NONE:
            log.error('Need a valid unique mac identifier')
            abort(400)

        try:
            q = model.Session.query(model.Station).filter(model.Station.mac == mac).one()
            model.Session.delete(q)
            model.Session.commit()
        except:
            abort(400)

        redirect_to('/admin/list_station_configurations')

    def list_initial_configurations(self):
        config_q = model.Session.query(model.Config)
        c.Configs = config_q.all()
        return render('/list_initial_configurations.mako')

    def list_station_configurations(self):
        config_q = model.Session.query(model.Station)
        c.Stations = config_q.all()
        return render('/list_station_configurations.mako')

    # CRUFT

    def _get_config_entry_by_id_or_mac_or_create(self, key):
        key = str(key)
        log.debug('_get_config_entry_by_id_or_mac_or_create(%s)' % key)
        conf = model.Session.query(model.Config)
        if len(key) == 12:
            # look for MAC
            try:
                q = conf.filter(model.Config.mac == key).one()
                log.debug('MAC found')
            except:
                q = model.Config()
                q.mac = key
                log.debug('MAC not found: create new config')
        else:
            # look for Primary Key
            q = conf.get(key)
            log.debug('Primary Key found')
        if q == None:
            q = model.Config()
        return q
       
    def _validate_configuration(self, config, is_edit):
        log.debug('config validation')
        error = {}

        if not is_edit:
            try:
                model.Session.query(model.Config).filter(model.Config.mac == config.mac).one()
                error['mac'] = 'MAC is already being used'
            except:
                pass

        if not h.validate_with_regexp(g.MAC_REGEXP, config.mac, True, log):
            error['mac'] = 'MAC address must be 12 hex lower case values, no separator' 
        if not h.validate_with_regexp(g.LANG_REGEXP, config.lang, True, log):
            error['lang'] = 'Must be a valid lang string. E.g. en_UK.utf-8'

        return error

    def _copy_reset_config(self, dir):
        for f in os.listdir(dir):
            if str(f).endswith('.tar.gz'):
                log.debug(dir + '../blank.tar.gz' + ' overwrites  ' + f)
                shutil.copyfile(dir + '../blank.tar.gz', dir + '/' + f)
    """


