import latex

trim = (30, 0, 50, 10)
width = 0.49
fig = latex.Figure(
    if_centering=False)

subf = latex.Subfigure(
    subfig_width = 0.45,
    trim = (30, 0, 130, 30),
    file = 'slip_d_simu_dip3_stk4.pdf',
    caption = ''
    )
fig.append_subfigure(subf)

subf = latex.Subfigure(
    subfig_width = 0.537,
    trim = trim,
    file = 'dip3_stk4_ano_11.pdf',
    caption = ''
    )
fig.append_subfigure(subf)

doc = latex.LatexDoc()
doc.elements = [fig]

cmpl = latex.PDFComplie(doc)
cmpl.compile('_checkerboard_test.pdf')
