// Main JavaScript for Task Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation enhancement
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Task status update functionality
    var statusSelects = document.querySelectorAll('.task-status-select');
    statusSelects.forEach(function(select) {
        select.addEventListener('change', function() {
            var taskId = this.dataset.taskId;
            var newStatus = this.value;
            updateTaskStatus(taskId, newStatus);
        });
    });

    // Priority color coding
    var priorityElements = document.querySelectorAll('[data-priority]');
    priorityElements.forEach(function(element) {
        var priority = element.dataset.priority;
        element.classList.add('priority-' + priority);
    });

    // Due date highlighting
    var dueDateElements = document.querySelectorAll('[data-due-date]');
    dueDateElements.forEach(function(element) {
        var dueDate = new Date(element.dataset.dueDate);
        var today = new Date();
        if (dueDate < today) {
            element.classList.add('text-danger', 'fw-bold');
        }
    });

    // Search functionality
    var searchInput = document.getElementById('task-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            var searchTerm = this.value.toLowerCase();
            var taskRows = document.querySelectorAll('.task-row');
            
            taskRows.forEach(function(row) {
                var taskTitle = row.querySelector('.task-title').textContent.toLowerCase();
                var taskDescription = row.querySelector('.task-description').textContent.toLowerCase();
                
                if (taskTitle.includes(searchTerm) || taskDescription.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // Filter functionality
    var filterSelects = document.querySelectorAll('.task-filter');
    filterSelects.forEach(function(select) {
        select.addEventListener('change', function() {
            applyFilters();
        });
    });

    // Sort functionality
    var sortSelect = document.getElementById('task-sort');
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            sortTasks(this.value);
        });
    }

    // Task creation form enhancement
    var taskForm = document.getElementById('task-form');
    if (taskForm) {
        var estimatedHoursInput = document.getElementById('id_estimated_hours');
        var actualHoursInput = document.getElementById('id_actual_hours');
        
        if (estimatedHoursInput && actualHoursInput) {
            estimatedHoursInput.addEventListener('input', function() {
                validateHours(this, actualHoursInput);
            });
            
            actualHoursInput.addEventListener('input', function() {
                validateHours(actualHoursInput, estimatedHoursInput);
            });
        }
    }

    // Comment system
    var commentForms = document.querySelectorAll('.comment-form');
    commentForms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            submitComment(this);
        });
    });

    // File upload enhancement
    var fileInputs = document.querySelectorAll('.file-upload');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            updateFileName(this);
        });
    });

    // Enhanced delete functionality
    var deleteButtons = document.querySelectorAll('.delete-task-btn');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            var taskId = this.dataset.taskId;
            var taskTitle = this.dataset.taskTitle;
            confirmTaskDeletion(taskId, taskTitle);
        });
    });

    // Responsive table handling
    var tables = document.querySelectorAll('.table-responsive');
    tables.forEach(function(table) {
        if (table.scrollWidth > table.clientWidth) {
            table.classList.add('has-scroll');
        }
    });

    // Dark mode toggle (if implemented)
    var darkModeToggle = document.getElementById('dark-mode-toggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('change', function() {
            toggleDarkMode(this.checked);
        });
    }
});

// Function to update task status via API
function updateTaskStatus(taskId, newStatus) {
    fetch(`/api/tasks/${taskId}/update_status/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            status: newStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            showNotification('Task status updated successfully!', 'success');
            updateTaskRow(taskId, newStatus);
        } else {
            showNotification('Failed to update task status.', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred while updating task status.', 'error');
    });
}

// Function to submit comments
function submitComment(form) {
    var formData = new FormData(form);
    var taskId = form.dataset.taskId;
    
    fetch(`/api/tasks/${taskId}/comments/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            showNotification('Comment added successfully!', 'success');
            addCommentToPage(data);
            form.reset();
        } else {
            showNotification('Failed to add comment.', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred while adding comment.', 'error');
    });
}

// Function to apply filters
function applyFilters() {
    var statusFilter = document.getElementById('status-filter').value;
    var priorityFilter = document.getElementById('priority-filter').value;
    var categoryFilter = document.getElementById('category-filter').value;
    
    var taskRows = document.querySelectorAll('.task-row');
    
    taskRows.forEach(function(row) {
        var status = row.dataset.status;
        var priority = row.dataset.priority;
        var category = row.dataset.category;
        
        var showRow = true;
        
        if (statusFilter && status !== statusFilter) showRow = false;
        if (priorityFilter && priority !== priorityFilter) showRow = false;
        if (categoryFilter && category !== categoryFilter) showRow = false;
        
        row.style.display = showRow ? '' : 'none';
    });
}

// Function to sort tasks
function sortTasks(sortBy) {
    var taskRows = Array.from(document.querySelectorAll('.task-row'));
    var tbody = document.querySelector('.task-table tbody');
    
    taskRows.sort(function(a, b) {
        var aValue, bValue;
        
        switch(sortBy) {
            case 'title':
                aValue = a.querySelector('.task-title').textContent;
                bValue = b.querySelector('.task-title').textContent;
                return aValue.localeCompare(bValue);
            case 'due_date':
                aValue = new Date(a.dataset.dueDate || '9999-12-31');
                bValue = new Date(b.dataset.dueDate || '9999-12-31');
                return aValue - bValue;
            case 'priority':
                var priorityOrder = { 'urgent': 4, 'high': 3, 'medium': 2, 'low': 1 };
                aValue = priorityOrder[a.dataset.priority] || 0;
                bValue = priorityOrder[b.dataset.priority] || 0;
                return bValue - aValue;
            case 'status':
                var statusOrder = { 'pending': 1, 'in_progress': 2, 'review': 3, 'completed': 4, 'cancelled': 5 };
                aValue = statusOrder[a.dataset.status] || 0;
                bValue = statusOrder[b.dataset.status] || 0;
                return aValue - bValue;
            default:
                return 0;
        }
    });
    
    taskRows.forEach(function(row) {
        tbody.appendChild(row);
    });
}

// Function to validate hours
function validateHours(input, compareInput) {
    var value = parseFloat(input.value);
    var compareValue = parseFloat(compareInput.value);
    
    if (value < 0) {
        input.setCustomValidity('Hours cannot be negative');
    } else if (compareInput.value && value > compareValue) {
        input.setCustomValidity('Actual hours cannot exceed estimated hours');
    } else {
        input.setCustomValidity('');
    }
}

// Function to update file name display
function updateFileName(input) {
    var fileName = input.files[0] ? input.files[0].name : 'No file chosen';
    var fileNameDisplay = input.parentNode.querySelector('.file-name');
    if (fileNameDisplay) {
        fileNameDisplay.textContent = fileName;
    }
}

// Function to show notifications
function showNotification(message, type) {
    var alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
    var icon = type === 'success' ? 'check-circle' : 'exclamation-triangle';
    
    var notification = document.createElement('div');
    notification.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        <i class="fas fa-${icon} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(function() {
        var bsAlert = new bootstrap.Alert(notification);
        bsAlert.close();
    }, 5000);
}

// Function to get CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to toggle dark mode
function toggleDarkMode(enabled) {
    if (enabled) {
        document.body.classList.add('dark-mode');
        localStorage.setItem('darkMode', 'enabled');
    } else {
        document.body.classList.remove('dark-mode');
        localStorage.setItem('darkMode', 'disabled');
    }
}

// Function to update task row after status change
function updateTaskRow(taskId, newStatus) {
    var taskRow = document.querySelector(`[data-task-id="${taskId}"]`);
    if (taskRow) {
        var statusBadge = taskRow.querySelector('.status-badge');
        if (statusBadge) {
            statusBadge.textContent = newStatus.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
            statusBadge.className = `badge status-badge bg-${getStatusColor(newStatus)}`;
        }
    }
}

// Function to get status color
function getStatusColor(status) {
    switch(status) {
        case 'completed': return 'success';
        case 'in_progress': return 'info';
        case 'review': return 'warning';
        case 'cancelled': return 'secondary';
        default: return 'secondary';
    }
}

// Function to add comment to page
function addCommentToPage(commentData) {
    var commentsContainer = document.querySelector('.comments-container');
    if (commentsContainer) {
        var commentHtml = `
            <div class="comment-item border-bottom pb-3 mb-3">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <h6 class="mb-1">${commentData.author.username}</h6>
                        <p class="mb-1">${commentData.content}</p>
                        <small class="text-muted">${new Date(commentData.created_at).toLocaleString()}</small>
                    </div>
                </div>
            </div>
        `;
        commentsContainer.insertAdjacentHTML('beforeend', commentHtml);
    }
}

// Function to confirm task deletion
function confirmTaskDeletion(taskId, taskTitle) {
    var modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.id = 'deleteConfirmModal';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header bg-danger text-white">
                    <h5 class="modal-title">
                        <i class="fas fa-exclamation-triangle me-2"></i>Confirm Deletion
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body text-center">
                    <i class="fas fa-trash fa-3x text-danger mb-3"></i>
                    <h6>Are you sure you want to delete this task?</h6>
                    <div class="alert alert-warning">
                        <strong>Task:</strong> ${taskTitle}
                        <br>
                        <small class="text-muted">This action cannot be undone.</small>
                    </div>
                </div>
                <div class="modal-footer justify-content-center">
                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">
                        <i class="fas fa-times me-2"></i>Cancel
                    </button>
                    <button type="button" class="btn btn-danger" onclick="deleteTask(${taskId})">
                        <i class="fas fa-trash me-2"></i>Delete Task
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    var bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    // Clean up modal after it's hidden
    modal.addEventListener('hidden.bs.modal', function() {
        document.body.removeChild(modal);
    });
}

// Function to delete task via API
function deleteTask(taskId) {
    // Show loading state
    var deleteBtn = document.querySelector(`[onclick="deleteTask(${taskId})"]`);
    var originalText = deleteBtn.innerHTML;
    deleteBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Deleting...';
    deleteBtn.disabled = true;
    
    fetch(`/tasks/${taskId}/delete/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (response.redirected) {
            // If there's a redirect, follow it
            window.location.href = response.url;
        } else if (response.ok) {
            // If successful, close modal and show success message
            var modal = bootstrap.Modal.getInstance(document.getElementById('deleteConfirmModal'));
            modal.hide();
            showNotification('Task deleted successfully!', 'success');
            
            // Remove task row from the page if we're on a list page
            var taskRow = document.querySelector(`[data-task-id="${taskId}"]`);
            if (taskRow) {
                taskRow.remove();
            }
            
            // Update task count if it exists
            var taskCount = document.querySelector('.task-count');
            if (taskCount) {
                var currentCount = parseInt(taskCount.textContent);
                taskCount.textContent = currentCount - 1;
            }
        } else {
            throw new Error('Failed to delete task');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred while deleting the task.', 'error');
        
        // Reset button state
        deleteBtn.innerHTML = originalText;
        deleteBtn.disabled = false;
    });
}

// Function to delete task directly from confirmation page
function deleteTaskDirectly(taskId, taskTitle) {
    // Show loading state
    var deleteBtn = document.querySelector(`[onclick="deleteTaskDirectly(${taskId}, '${taskTitle}')"]`);
    var originalText = deleteBtn.innerHTML;
    deleteBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Deleting...';
    deleteBtn.disabled = true;
    
    fetch(`/tasks/${taskId}/delete/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (response.redirected) {
            // If there's a redirect, follow it
            window.location.href = response.url;
        } else if (response.ok) {
            // If successful, show success message and redirect to task list
            showNotification('Task deleted successfully!', 'success');
            
            // Redirect to task list after a short delay
            setTimeout(function() {
                window.location.href = '/tasks/';
            }, 1000);
        } else {
            throw new Error('Failed to delete task');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred while deleting the task.', 'error');
        
        // Reset button state
        deleteBtn.innerHTML = originalText;
        deleteBtn.disabled = false;
    });
}

// Export functions for use in other scripts
window.TaskManager = {
    updateTaskStatus: updateTaskStatus,
    submitComment: submitComment,
    applyFilters: applyFilters,
    sortTasks: sortTasks,
    showNotification: showNotification,
    confirmTaskDeletion: confirmTaskDeletion,
    deleteTask: deleteTask,
    deleteTaskDirectly: deleteTaskDirectly
}; 