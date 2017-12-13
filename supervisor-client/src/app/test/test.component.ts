import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import 'brace';
import 'brace/mode/json';
import 'brace/theme/eclipse';
import { TestService } from '../store/services/test.service';
import { ValuesPipe } from 'ngx-pipes';

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css']
})
export class TestComponent implements OnInit {
  taskID;
  code: string = '';
  constructor(
    private route: ActivatedRoute,
    private location: Location,
    private _testService: TestService
  ) {
    this._testService.currentQueryResult$.subscribe(result => {
      this.queryResult = result;
      console.log('HERE:', this.queryResult);
    });
  }
  theme = 'eclipse';
  languageMode = 'javascript';
  options = {
    minLines: 50,
    maxLines: 37,
    enableBasicAutocompletion: true,
    enableLiveAutocompletion: true,
    displayIndentGuides: false,
    showInvisibles: true,
    scrollPastEnd: true
  };

  queryResult;

  submitQuery() {
    this._testService.submitQuery(this.taskID, this.code);
  }

  onChange() {
    console.log(this.code);
  }

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    this.taskID = id;
  }
}
