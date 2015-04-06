import latex

from sites import sites_names

fig = latex.Figure(if_centering=False)

subfig_width = 0.33
incl_width = 1.

trim = (20,45,20,-10)

site = 'J162'
for cmpt in 'e', 'n', 'u':
    subf = latex.Subfigure(
        subfig_width = subfig_width,
        incl_width = incl_width,
        trim = trim,
        file = 'plots/%s-%s-post.pdf'%(site, cmpt),
        caption = ''
        )
    fig.append_subfigure(subf)

site = 'J059'
for cmpt in 'e', 'n':
    subf = latex.Subfigure(
        subfig_width = subfig_width,
        incl_width = incl_width,
        trim = trim,
        file = 'plots/%s-%s-post.pdf'%(site, cmpt),
        caption = ''
        )
    fig.append_subfigure(subf)
fig.append_subfigure(latex.NextParagraph())

for cmpt in 'e', 'n':
    subf = latex.Subfigure(
        subfig_width = subfig_width,
        incl_width = incl_width,
        trim = trim,
        file = 'plots/%s-%s-vel.pdf'%(site, cmpt),
        caption = ''
        )
    fig.append_subfigure(subf)
fig.append_subfigure(latex.NextParagraph())

site = 'CHAN'
for cmpt in 'e', 'n':
    subf = latex.Subfigure(
        subfig_width = subfig_width,
        incl_width = incl_width,
        trim = trim,
        file = 'plots/%s-%s-post.pdf'%(site, cmpt),
        caption = ''
        )
    fig.append_subfigure(subf)

fig.append_subfigure(
    latex.Subfigure(
        subfig_width = 0.3,
        incl_width = 1.,
        trim = (50,30,50,470),
        file='time_series_stations',
        caption = ''
        )
    )

doc = latex.LatexDoc()
doc.elements = [fig]


cmpl = latex.PDFComplie(doc)
cmpl.compile("_onland_time_series.pdf")
