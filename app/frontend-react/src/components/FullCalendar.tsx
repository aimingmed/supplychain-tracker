import React from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import type { CalendarEvent } from '../types';

interface FullCalendarComponentProps {
  events?: CalendarEvent[];
  onEventClick?: (info: any) => void;
  onDateClick?: (info: any) => void;
  height?: string | number;
  initialView?: 'dayGridMonth' | 'timeGridWeek' | 'timeGridDay';
}

const FullCalendarComponent: React.FC<FullCalendarComponentProps> = ({
  events = [],
  onEventClick,
  onDateClick,
  height = 'auto',
  initialView = 'dayGridMonth'
}) => {
  return (
    <div className="bg-white rounded-lg border">
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView={initialView}
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        }}
        events={events}
        editable={true}
        selectable={true}
        selectMirror={true}
        dayMaxEvents={true}
        weekends={true}
        eventClick={onEventClick}
        dateClick={onDateClick}
        height={height}
        locale="zh-cn"
        buttonText={{
          today: '今天',
          month: '月',
          week: '周',
          day: '日'
        }}
        dayHeaderFormat={{ weekday: 'short' }}
        slotLabelFormat={{
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        }}
        eventTimeFormat={{
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        }}
      />
    </div>
  );
};

export default FullCalendarComponent;
