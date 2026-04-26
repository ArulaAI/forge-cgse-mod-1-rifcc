import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  template: `
    <div class="container">
      <div class="warning-banner">
        <strong>Warning:</strong> This application contains intentional security vulnerabilities for educational purposes.
        <strong>DO NOT</strong> use this code in production!
      </div>
      <h1>CGSE Lab 1 - Angular</h1>
      <router-outlet></router-outlet>
    </div>
  `,
  styles: [`
    h1 {
      color: #333;
      margin-bottom: 20px;
    }
  `]
})
export class AppComponent {
  title = 'cgse-lab1-angular';
}
