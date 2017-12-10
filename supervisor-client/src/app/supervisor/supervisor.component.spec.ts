import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SupervisorComponent } from './supervisor.component';

describe('SupervisorComponent', () => {
  let component: SupervisorComponent;
  let fixture: ComponentFixture<SupervisorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SupervisorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SupervisorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
