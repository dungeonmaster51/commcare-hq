# Third-Party Libraries

## jQuery
[jQuery](https://jquery.com/) is available throughout HQ. We use jQuery 3 everywhere except in Web Apps, which depends on [marionette](https://marionettejs.com/) v2, which is only compatible with jQuery 2.

Prefix jQuery variables with a `$`:
```
var $rows = $("#myTable tr"),
    firstRow = $rows[0];
```

## Underscore
[Underscore](http://underscorejs.org/) is available throughout HQ for utilities.

## Knockout
[Knockout](http://knockoutjs.com/) is also available throughout HQ and should be used for new code. We use Knockout 3.0.

Prefix knockout observables with an `o`:

```
var myModel = function (options) {
    var self = this;
    self.type = options.type;
    self.oTotal = ko.observable(0);
};
```

...so that in HTML it's apparent what you're dealing with:

```
<input data-bind="visible: type === 'large' && oTotal() > 10, value: oTotal" />

Current total: <span data-bind="text: oTotal"></div>
```

## Backbone
[Backbone](http://backbonejs.org/) is used in Web Apps. It **should not** be used outside of Web Apps.

## Angular
[Angular](https://angularjs.org/) is used only in custom reports for ICDS. It **should not** be used for new code. The angular we do have is Angular 1, which is outdated but is effectively a different framework than later versions of angular, making upgrading non-trivial. It's [unclear](https://toddmotto.com/future-of-angular-1-x#whats-next-for-angular-1x) how long Angular 1 will be supported by its creators.

## Yarn
We use [yarn](https://classic.yarnpkg.com/en/) for package management, so new libraries should be added to [package.json](https://github.com/dimagi/commcare-hq/blob/master/package.json).
