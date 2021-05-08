import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import data from './ISentiment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass'],
})
export class AppComponent {
  constructor(private http: HttpClient) {}

  sentence: string;
  results: data = undefined;
  loading: boolean = false;

  submit() {
    this.loading = true;
    this.results = undefined;

    this.http
      .post('http://localhost:8000/api/sentiment', {
        sentence: this.sentence,
      })
      .subscribe((res) => {
        this.results = res as data;
        this.loading = false;
      });
  }

  getGreen() {
    const res = {
      width: this.results ? Math.round(this.results.pos * 100) + '%' : '0%',
    };

    return res;
  }

  getRed() {
    const res = {
      width: this.results ? Math.round(this.results.neg * 100) + '%' : '0%',
    };

    return res;
  }

  getGray() {
    const res = {
      width: this.results ? Math.round(this.results.neu * 100) + '%' : '0%',
    };
    return res;
  }

  getResult() {
    if (this.results) {
      const { pos, neu, neg } = this.results;
      const max = Math.max.apply(null, [pos, neu, neg]);

      const map = {
        pos: 'positive',
        neg: 'negative',
        neu: 'neutral',
      };

      const x = Object.keys(this.results).filter(
        (item) => this.results[item] == max
      )[0];

      return map[x] || 'None';
    }
  }
}
