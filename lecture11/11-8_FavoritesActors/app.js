import {MDCTopAppBar} from '@material/top-app-bar';

const topAppBarElement = document.querySelector('.mdc-top-app-bar');
const topAppBar = new MDCTopAppBar(topAppBarElement);

import {MDCTabBar} from '@material/tab-bar';

const tabBar = new MDCTabBar(document.querySelector('.mdc-tab-bar'));

tabBar.listen('MDCTabBar:activated', (activatedEvent) => {
  document.querySelectorAll('.mdc-layout-grid').forEach((element, index) => {
    if (index === activatedEvent.detail.index) {
      element.classList.remove('mdc-layout-grid--hidden');
    } else {
      element.classList.add('mdc-layout-grid--hidden');
    }
  });
});