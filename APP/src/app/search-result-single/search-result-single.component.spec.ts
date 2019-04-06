import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {SearchResultSingleComponent} from './search-result-single.component';

describe('SearchResultSingleComponent', () => {
  let component: SearchResultSingleComponent;
  let fixture: ComponentFixture<SearchResultSingleComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SearchResultSingleComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchResultSingleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
