import latex

trim = (120, 40, 50, 220)

subfig_width = 0.45
incl_width = .6
fig = latex.Figure()

fig.append_subfigure(
    latex.Subfigure(subfig_width=subfig_width, trim=trim, rotation = -90,
                    incl_width = incl_width,
                    file='co_post_obs.pdf',
                    caption='')
    )

fig.append_subfigure(
    latex.Subfigure(subfig_width=subfig_width, trim=trim, rotation = -90,
                    incl_width = incl_width,
                    file='co_obs_pred.pdf',caption='')
    )

fig.append_subfigure(
    latex.Subfigure(subfig_width=subfig_width, trim=trim, rotation = -90,
                    incl_width = incl_width,
                    file='post_obs_pred_slip_only.pdf',caption='')
    )

fig.append_subfigure(
    latex.Subfigure(subfig_width=subfig_width, trim=trim, rotation = -90,
                    incl_width = incl_width,
                    file='post_obs_pred_coupled.pdf', caption='')
    )

fig.append_subfigure(
    latex.Subfigure(subfig_width=0.2, trim=(60, 60, 50, 300),
                    incl_width = 1,
                    file='location.pdf')
    )


doc = latex.LatexDoc()
doc.elements = [fig]

cmpl = latex.PDFComplie(doc)
cmpl.compile('_azi_diff_southwestern_honshu.pdf')
