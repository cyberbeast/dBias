import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.css']
})
export class ReportComponent implements OnInit {
  constructor(private route: ActivatedRoute, private location: Location) {}

  ngOnInit() {
    this.getReport();
  }

  o_id;

  getReport() {
    const id = this.route.snapshot.paramMap.get('id');
    this.o_id = id;
  }
}
