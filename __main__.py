from modules.facility import facility

detroit = facility('DETROITMI')

rmi = detroit.rmi
cfr = detroit.cfr
pfi = detroit.pfi
pfo = detroit.pfo
pis = detroit.pis
pck = detroit.pck

time = 0
transfer = pd.DataFrame(
    {
        'jb_color':['Coloring Agent1', 'Coloring Agent18'],
        'amount':[45000, 250000]
    }
)
rmi.load_drums(transfer, time=time)

flavors = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15']
flavor = (flavor for flavor in flavors)

package_types = ['Box', 'Box', 'Box', 'Bag', 'Bag']
package_type = (pack for pack in package_types)

while len(pis.empty_drums)!=0:
    pck_in = next(pis.unload_drums())
    pck_in['package_type'] = next(package_type)
    pck_time = pck.load_machines(**pck_in)
    print("Packing Time: {0}".format(pck_time))
    time += pck_time
    print("Global Time: {0}".format(time))

    while len(pfo.avail_mach)!=0:
        pis_cap = min([x.capacity for x in pis.empty_drums])
        pfo_out = next(pfo.unload_machines(pis_cap))
        pis.load_drums(pfo_out, time=time)

        while len(pfi.empty_drums)!=0:
            pfo_in = next(pfi.unload_drums())
            pfo_in['jb_flavor'] = next(flavor)
            pfo_time = pfo.load_machines(**pfo_in)
            print("PFO Time: {0}".format(pfo_time))
            time += pfo_time
            print("Global Time: {0}".format(time))

            while len(cfr.avail_mach)!=0:
                pfi_cap = min([x.capacity for x in pfi.empty_drums])
                cfr_out = next(cfr.unload_machines(pfi_cap))
                pfi.load_drums(cfr_out, time=time)

                while len(rmi.empty_drums)!=0:
                    cfr_in = next(rmi.unload_drums())
                    cfr_time = cfr.load_machines(**cfr_in)
                    print("Classifier Time: {0}".format(cfr_time))
                    time += cfr_time
                    print("Global Time: {0}".format(time))

                else:
                    break
            else:
                break
        else:
            break
    else:
        break
