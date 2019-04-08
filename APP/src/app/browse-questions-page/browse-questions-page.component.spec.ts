import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {BrowseQuestionsPageComponent} from './browse-questions-page.component';

describe('BrowseQuestionsPageComponent', () => {
  let component: BrowseQuestionsPageComponent;
  let fixture: ComponentFixture<BrowseQuestionsPageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BrowseQuestionsPageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BrowseQuestionsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
