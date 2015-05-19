import viscojapan as vj

fn = '/home/zy/workspace/viscojapan/inversions/inversion11/iter1/run0/outs/nrough_06_naslip_11.h5'

reader = vj.inv.ResultFileReader(fn)

slip = reader.get_slip()

for ext in '.pdf', '.png':
    plt = vj.slip.plot.plot_slip_overview(
        slip,
        'slip_overview' + ext,
        if_x_log=False,
        xlim=[0, 1344],
        ylim=[0,85],
        yticks=[20,40,60],
        xticks = [500, 1000],
        xticklabels = [r'500', r'1000'],
        )
