import {animate, style, transition, trigger} from '@angular/animations';

export const fold = trigger(
  'enterAnimation', [
    transition(':enter', [
      style({maxHeight: '0', opacity: 0}),
      animate('{{time}}', style({maxHeight: '{{h}}', opacity: 1}))
    ]),
    transition(':leave', [
      style({maxHeight: '{{h}}', opacity: 1}),
      animate('500ms', style({maxHeight: '0', opacity: 0}))
    ])
  ]
)
export const slide = trigger(
  'enterAnimation', [
    transition(':enter', [
      style({transform: 'translateX(100%)', opacity: 0}),
      animate('{{time}}', style({transform: 'translateX(0%)', opacity: 1}))
    ]),
    transition(':leave', [
      style({transform: 'translateX(0%)', opacity: 1}),
      animate('500ms', style({transform: 'translateX(-100%)', opacity: 0}))
    ])
  ]
)
