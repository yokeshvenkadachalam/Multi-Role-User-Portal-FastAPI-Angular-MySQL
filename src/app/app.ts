import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  template: `
  <div class="page-container fade-in">
    <div class="portal-card slide-up">

      <!-- Login / Signup -->
      <div *ngIf="!loggedIn" class="fade-in">
        <h1 class="title">Web Portal</h1>

        <div *ngIf="view==='home'" class="center-buttons fade-in">
          <button class="btn primary" (click)="view='signup'">Sign Up</button>
          <button class="btn secondary" (click)="view='signin'">Sign In</button>
        </div>

        <div *ngIf="view==='signup'" class="fade-in">
          <h2 class="subtitle">Create an account</h2>
          <input [(ngModel)]="signupName" placeholder="Full Name" class="input"/>
          <input [(ngModel)]="signupEmail" placeholder="Email" class="input"/>
          <select [(ngModel)]="signupRole" class="input">
            <option value="student">Student</option>
            <option value="employee">Employee</option>
            <option value="manager">Manager</option>
            <option value="entrepreneur">Entrepreneur</option>
            <option value="jobseeker">Jobseeker</option>
          </select>
          <div class="form-actions">
            <button class="btn primary" (click)="signup()">Sign Up</button>
            <button class="btn link" (click)="view='home'">Back</button>
          </div>
        </div>

        <div *ngIf="view==='signin'" class="fade-in">
          <h2 class="subtitle">Welcome Back</h2>
          <input [(ngModel)]="signinLoginId" placeholder="Login ID" class="input"/>
          <input [(ngModel)]="signinPassword" type="password" placeholder="Password" class="input"/>
          <div class="form-actions">
            <button class="btn primary" (click)="signin()">Sign In</button>
            <button class="btn link" (click)="view='home'">Back</button>
          </div>
        </div>
      </div>
      <div *ngIf="loggedIn" class="fade-in">
        <h1 class="title">Welcome, {{userData?.name}}</h1>
        <div *ngIf="page==='fill'" class="fade-in">
          <h2 class="subtitle">{{profile?.student ? 'Edit Student Details' : 'Fill Student Details'}}</h2>

          <div class="grid-2">
            <input [(ngModel)]="student.first_name" placeholder="First Name" class="input"/>
            <input [(ngModel)]="student.last_name" placeholder="Last Name" class="input"/>
          </div>

          <input [(ngModel)]="student.email" placeholder="Email" class="input"/>
          <input [(ngModel)]="student.mobile" placeholder="Mobile" class="input"/>

          <div class="gender-group">
            <span>Gender:</span>
            <label><input type="radio" [(ngModel)]="student.gender" name="gender" value="Male"> Male</label>
            <label><input type="radio" [(ngModel)]="student.gender" name="gender" value="Female"> Female</label>
            <label><input type="radio" [(ngModel)]="student.gender" name="gender" value="Other"> Other</label>
          </div>

          <input [(ngModel)]="student.current_location" placeholder="Current Location" class="input"/>
          <input [(ngModel)]="student.permanent_address" placeholder="Permanent Address" class="input"/>
          <input [(ngModel)]="student.college_name" placeholder="College Name" class="input"/>
          <input [(ngModel)]="student.school_name" placeholder="School Name" class="input"/>

          <label class="file-label">
            Photo: <input type="file" (change)="onFileChange($event,'photo')"/>
          </label>
          <label class="file-label">
            Resume (PDF): <input type="file" (change)="onFileChange($event,'resume')"/>
          </label>

          <div class="form-actions">
            <button class="btn primary" (click)="submitStudent()">Save</button>
          </div>
        </div>
        <div *ngIf="page==='view' && profile" class="profile-section fade-in">
          <h2 class="subtitle">Profile</h2>
          <div class="profile-card">
            <div class="profile-left">
              <img *ngIf="profile.student?.photo"
                   [src]="'data:image/jpeg;base64,'+profile.student.photo"
                   alt="Profile Photo"/>
              <div *ngIf="profile.student?.resume">
                <a [href]="'data:application/pdf;base64,'+profile.student.resume"
                   download="resume.pdf"
                   class="btn secondary resume-btn">
                   Download Resume
                </a>
              </div>
            </div>
            <div class="profile-right">
              <p><strong>Name:</strong> {{profile.user.name}}</p>
              <p><strong>Email:</strong> {{profile.user.email}}</p>
              <p><strong>Role:</strong> {{profile.user.role}}</p>
              <p><strong>Full Name:</strong> {{profile.student.first_name}} {{profile.student.last_name}}</p>
              <p><strong>Mobile:</strong> {{profile.student.mobile}}</p>
              <p><strong>Gender:</strong> {{profile.student.gender}}</p>
              <p><strong>College:</strong> {{profile.student.college_name}}</p>
              <p><strong>School:</strong> {{profile.student.school_name}}</p>
            </div>
          </div>
          <div class="form-actions">
            <button class="btn secondary" (click)="page='fill'">Edit Profile</button>
            <button class="btn danger" (click)="logout()">Logout</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  `,
  styles: [`
    .page-container {
      background: linear-gradient(135deg, #f1f2f6, #dfe4ea);
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 2rem;
    }
    .portal-card {
      background: #fff;
      border-radius: 18px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.08);
      padding: 2.5rem 3rem;
      width: 100%;
      max-width: 700px;
      transition: all 0.3s ease-in-out;
    }
    .title {
      text-align: center;
      font-size: 2rem;
      font-weight: 700;
      color: #2d3436;
      margin-bottom: 1rem;
    }
    .subtitle {
      font-size: 1.3rem;
      font-weight: 600;
      color: #2c3e50;
      margin-bottom: 1.2rem;
      border-bottom: 2px solid #3498db20;
      padding-bottom: 0.3rem;
    }
    .input {
      width: 100%;
      padding: 0.75rem 1rem;
      margin: 0.5rem 0;
      border: 1px solid #dcdde1;
      border-radius: 10px;
      font-size: 1rem;
      transition: all 0.2s ease;
    }
    .input:focus {
      border-color: #3498db;
      outline: none;
      box-shadow: 0 0 0 3px rgba(52,152,219,0.1);
    }
    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.6rem;
    }
    .gender-group {
      display: flex;
      gap: 1rem;
      align-items: center;
      font-size: 0.95rem;
      color: #555;
      margin: 0.6rem 0;
    }
    .file-label {
      font-size: 0.9rem;
      color: #555;
      display: block;
      margin-top: 0.8rem;
    }
    .btn {
      border: none;
      border-radius: 10px;
      padding: 0.7rem 1.2rem;
      font-size: 1rem;
      cursor: pointer;
      transition: all 0.2s ease-in-out;
    }
    .btn.primary { background: #3498db; color: white; }
    .btn.primary:hover { background: #2980b9; transform: translateY(-1px); }
    .btn.secondary { background: #95a5a6; color: white; }
    .btn.secondary:hover { background: #7f8c8d; transform: translateY(-1px); }
    .btn.danger { background: #e74c3c; color: white; }
    .btn.danger:hover { background: #c0392b; transform: translateY(-1px); }
    .btn.link { background: none; color: #3498db; text-decoration: underline; }
    .resume-btn { margin-top: 1rem; display: inline-block; }
    .center-buttons {
      display: flex;
      flex-direction: column;
      gap: 0.8rem;
    }
    .form-actions {
      display: flex;
      justify-content: space-between;
      margin-top: 1.2rem;
    }
    .profile-card {
      display: flex;
      flex-wrap: wrap;
      background: #f8f9fa;
      padding: 1.5rem;
      border-radius: 12px;
      gap: 1rem;
      box-shadow: inset 0 0 5px rgba(0,0,0,0.02);
    }
    .profile-left {
      flex: 1;
      text-align: center;
    }
    .profile-left img {
      max-width: 160px;
      border-radius: 12px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
      margin-bottom: 1rem;
    }
    .profile-right {
      flex: 2;
      font-size: 1rem;
      color: #333;
      line-height: 1.6;
    }
    /* Animations */
    .fade-in { animation: fadeIn 0.5s ease forwards; }
    .slide-up { animation: slideUp 0.5s ease forwards; }
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    @keyframes slideUp {
      from { transform: translateY(20px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
  `]
})
export class AppComponent {
  view:'home'|'signup'|'signin' = 'home';
  loggedIn=false;
  page:'fill'|'view'='fill';

  signupName=''; signupEmail=''; signupRole='student';
  signinLoginId=''; signinPassword='';

  userData:any=null;
  profile:any=null;

  student:any = {
    first_name:'', last_name:'', email:'', mobile:'', gender:'',
    current_location:'', permanent_address:'', college_name:'',
    school_name:'', photo:null, resume:null
  };

  constructor(private http: HttpClient) {}

  signup() {
    this.http.post('http://localhost:8000/api/signup',
      {name:this.signupName, email:this.signupEmail, role:this.signupRole})
    .subscribe((res:any) => { alert(res.message); this.view='signin'; });
  }

  signin() {
    this.http.post('http://localhost:8000/api/signin',
      {login_id:this.signinLoginId, password:this.signinPassword})
    .subscribe((res:any) => {
      this.loggedIn = true;
      this.userData = res;
      this.getProfile();
    });
  }

  logout() {
    this.loggedIn = false;
    this.userData = null;
    this.view = 'home';
    this.page = 'fill';
  }

  getProfile() {
    this.http.get(`http://localhost:8000/api/profile/${this.userData.user_id}`)
      .subscribe((res:any)=>{
        this.profile = res;
        if (res.student) {
          this.student = {...res.student};
          this.page = 'view';
        } else {
          this.page = 'fill';
        }
      });
  }

  onFileChange(event: Event, field: string) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.student[field] = input.files[0];
    }
  }

  submitStudent() {
    const fd = new FormData();
    Object.entries(this.student).forEach(([k,v]:any)=> {
      if (v !== null && v !== undefined) fd.append(k, v);
    });
    fd.append('user_id', this.userData.user_id);
    this.http.post('http://localhost:8000/api/students', fd)
      .subscribe(()=>{ alert('Saved successfully'); this.getProfile(); });
  }
}
