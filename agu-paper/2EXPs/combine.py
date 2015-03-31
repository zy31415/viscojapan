import latex

trim = (30, 0, 50, 10)
width = 0.49
fig = latex.Figure(
    if_centering=False)

subf = latex.Subfigure(
    subfig_width = width,
    trim = trim,
    file = 'Model_2EXPs_J550-e.pdf',
    caption = ''
    )
fig.append_subfigure(subf)

subf = latex.Subfigure(
    subfig_width = width,
    trim = trim,
    file = 'Model_EXP_J550-e.pdf',
    caption = ''
    )
fig.append_subfigure(subf)

subf = latex.Subfigure(
    subfig_width = width,
    trim = (30, 40, 50, 5),
    file = 'model_prediction_J550-e.pdf',
    caption = ''
    )
fig.append_subfigure(subf)

doc = latex.LatexDoc()
doc.elements = [fig]

cmpl = latex.PDFComplie(doc)
cmpl.compile('_2EXPs_EXP_pred.pdf')
