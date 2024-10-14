import { LitElement, html, css } from 'lit';
import { customElement, property } from 'lit/decorators.js';
import { repeat } from 'lit/directives/repeat.js';

// Define the structure of the group data
interface GroupData {
  id: number;
  groupName: string;
  members: Array<Member>;
}

interface Member {
  id: number;
  name: string;
}

@customElement('classes-list')
export class ClassesList extends LitElement {
  @property({ type: Array }) members: Member[] = [];

  static styles = css`
    .student {
      padding: 16px;
      margin: 10px 0;
      background-color: #f0f0f0;
      border-radius: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .student.present {
      background-color: #d4edda;
    }

    .student.absent {
      background-color: #f8d7da;
    }

    .swipeable {
      touch-action: pan-x;
    }
  `;

  firstUpdated() {
    this.fetchGroupData();
  }

async fetchGroupData() {
  const username = 'reka';
  const password = 'B1a9l8i8';
  const authString = btoa(`${username}:${password}`);


  console.log('Fetching group data...');

  try {
    const response = await fetch('http://127.0.0.1:8000/group/1', {
      headers: {
        'Authorization': `Basic ${authString}`,
                'Content-Type': 'application/json'  // Ensure Content-Type is correct
      }
    });

    console.log('Response status:', response.status);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: GroupData = await response.json();
    console.log('Data received:', data);

    this.members = data.members;
    console.log('Members set:', this.members);
  } catch (error) {
    console.error('Error fetching group data:', error);
  }
}



  handleSwipe(event: TouchEvent, member: Member) {
    const swipeDistance = 100; // Adjust this based on sensitivity
    const touchStartX = event.changedTouches[0].clientX;

    const touchEndHandler = (e: TouchEvent) => {
      const touchEndX = e.changedTouches[0].clientX;
      const distanceMoved = touchEndX - touchStartX;

      // Swipe right (present)
      if (distanceMoved > swipeDistance) {
        this.markPresent(member);
      }
      // Swipe left (absent)
      else if (distanceMoved < -swipeDistance) {
        this.markAbsent(member);
      }

      // Remove touchend listener
      this.removeEventListener('touchend', touchEndHandler);
    };

    this.addEventListener('touchend', touchEndHandler);
  }

  markPresent(member: Member) {
    const index = this.members.findIndex((m) => m.id === member.id);
    if (index !== -1) {
      this.shadowRoot?.querySelector(`#student-${member.id}`)?.classList.add('present');
    }
  }

  markAbsent(member: Member) {
    const index = this.members.findIndex((m) => m.id === member.id);
    if (index !== -1) {
      this.shadowRoot?.querySelector(`#student-${member.id}`)?.classList.add('absent');
    }
  }

  render() {
    return html`
      <div>
        <h1>Class List</h1>
        egyáltalán betölt...
        ${repeat(
          this.members,
          (member) => member.id,
          (member) => html`
            <div
              id="student-${member.id}"
              class="student swipeable"
              @touchstart="${(e: TouchEvent) => this.handleSwipe(e, member)}"
            >
              <span>${member.name}</span>
            </div>
          `
        )}
      </div>
    `;
  }
}
