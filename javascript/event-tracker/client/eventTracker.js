// eventTracker.js
(function() {
    const sendEvent = async (eventData) => {
      try {
        await fetch('https://your-server.com/track', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(eventData)
        });
      } catch (error) {
        console.error('Error sending event:', error);
      }
    };
  
    const trackEvent = (eventType, eventName, eventValue, additionalData = {}) => {
      const eventData = {
        event_id: crypto.randomUUID(), // Generate a unique event ID
        event_type: eventType,
        event_name: eventName,
        event_value: eventValue,
        event_starttime: new Date().toISOString(),
        event_createdtime: new Date().toISOString(),
        event_lat: additionalData.lat || null,
        event_lang: additionalData.lang || null,
        event_device: navigator.userAgent,
        event_website: window.location.hostname,
        browser: navigator.userAgent,
        os: navigator.platform,
        ip: additionalData.ip || null, // IP should be anonymized on the server
        ...additionalData
      };
  
      // Asynchronous logging
      sendEvent(eventData);
    };
  
    // Track page views
    trackEvent('page_view', 'page_load', window.location.href);
  
    // Track clicks
    document.addEventListener('click', (e) => {
      trackEvent('click', e.target.tagName, e.target.innerText, {
        elementId: e.target.id,
        elementClass: e.target.className
      });
    });
  
    // Track form submissions
    document.addEventListener('submit', (e) => {
      trackEvent('form_submit', e.target.id, 'form_submitted', {
        formData: Object.fromEntries(new FormData(e.target))
      });
    });
  
    // Track scrolls
    let scrollTimeout;
    window.addEventListener('scroll', () => {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(() => {
        trackEvent('scroll', 'page_scroll', window.scrollY);
      }, 100);
    });
  
    // Expose trackEvent to the global scope for custom events
    window.trackEvent = trackEvent;
  })();