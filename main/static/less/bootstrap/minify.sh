# Minify the bootstrap less files. This is really useful if you want to use the javascript version of less which makes a request for each of the following files. Note that variables.less is excluded from the bootstrap.less when minifying.

echo '@import "mixins.min.less"' > bootstrap.min.less
cat normalize.less print.less glyphicons.less scaffolding.less type.less\
    code.less grid.less tables.less forms.less buttons.less component-animations.less\
    dropdowns.less button-groups.less input-groups.less navs.less navbar.less breadcrumbs.less\
    pagination.less pager.less labels.less badges.less jumbotron.less thumbnails.less\
    alerts.less progress-bars.less media.less list-group.less panels.less\
    responsive-embed.less wells.less close.less modals.less tooltip.less popovers.less\
    carousel.less utilities.less responsive-utilities.less > bootstrap.min.less
cat mixins/hide-text.less mixins/opacity.less mixins/image.less mixins/labels.less\
    mixins/reset-filter.less mixins/resize.less mixins/responsive-visibility.less\
    mixins/size.less mixins/tab-focus.less mixins/text-emphasis.less mixins/text-overflow.less\
    mixins/vendor-prefixes.less mixins/alerts.less mixins/buttons.less mixins/panels.less\
    mixins/pagination.less mixins/list-group.less mixins/nav-divider.less mixins/forms.less\
    mixins/progress-bar.less mixins/table-row.less mixins/background-variant.less\
    mixins/border-radius.less mixins/gradients.less mixins/clearfix.less\
    mixins/center-block.less mixins/nav-vertical-align.less mixins/grid-framework.less\
    mixins/grid.less > mixins.min.less
