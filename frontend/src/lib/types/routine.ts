export interface Task {
  id: string;
  title: string;
  due: string;
}

export interface TaskList {
  id: string;
  title: string;
  tasks: Task[];
}

export interface Event {
  id: string;
  title: string;
  start: string;
  end: string;
  location: string;
}