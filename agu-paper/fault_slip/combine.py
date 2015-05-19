import latex

trim = (10, 0, 40, 5)
subfig_width = 0.49
incl_width = 1.

fig = latex.Figure()

fig.append_subfigure(
    latex.Subfigure(
        subfig_width = 1,
        incl_width = 1,
        trim=(30, 470, 120, 20),
        caption='',
        file='nrough_06_naslip_11.pdf')
    )

fig.append_subfigure(
    latex.Subfigure(
        subfig_width = 0.4,
        incl_width = incl_width,
        caption='',
        trim=(10, 10, 10, 30), file='mos_mws_nrough_06_naslip_11.pdf')
    )
doc = latex.LatexDoc()
doc.elements = [fig]

cmpl = latex.PDFComplie(doc)
cmpl.save('_fault_slip.pdf')
cmpl.save('_fault_slip.png')
