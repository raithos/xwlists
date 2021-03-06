import myapp
from persistence import Pilot, Upgrade
import xwingmetadata

if __name__ == "__main__":

    ships = xwingmetadata.ships
    session = myapp.db_connector.get_session()

    for ship_type in ships.keys():
        pilots = ships[ship_type]
        for pilot in pilots:
            db_pilot = session.query(Pilot).filter(Pilot.name == pilot['name']).first()

            if db_pilot is None:
                # print "New pilot!"
                sql = "insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( '%s','%s', '%d', '%d' );" % \
                      (pilot['name'], pilot['canon_name'], pilot['cost'], pilot['pilot_skill'])
                print sql
                sql = "insert  ship_pilot ( ship_type, pilot_id) select '%s', id from pilot where name='%s' and canon_name='%s';" % \
                      (xwingmetadata.canonize(ship_type), pilot['name'], pilot['canon_name'])
                print sql


            else:
                #print "I've seen you before!"
                continue

    upgrades = xwingmetadata.upgrades
    for upgrade_type in upgrades.keys():
        for upgrade in upgrades[upgrade_type]:
            db_upgrade = session.query(Upgrade).filter(Upgrade.name == upgrade['name']).first()
            if db_upgrade is None:
                if upgrade.has_key('type') and upgrade['type'] is not None:
                    sql = "insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( '%s', '%s', '%s', '%d');" % \
                          (upgrade['type'], upgrade['name'], upgrade['canon_name'], upgrade['cost'])
                    print sql
