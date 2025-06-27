$(document).ready(function () {
    const body = $('body');

    // Initialize theme from cookie
    const theme = getCookie('theme') || 'light';
    body.addClass('theme');
    if (theme === 'dark') {
        body.addClass('dark');
    } else {
        body.removeClass('dark');
    }

    // Toggle dark mode on button click
    $('#theme-toggle').click(function () {
        body.toggleClass('dark');
        const newTheme = body.hasClass('dark') ? 'dark' : 'light';
        setCookie('theme', newTheme, 30);
    });

    // Load courses dynamically if #courses exists
    if ($('#courses').length) {
        $.get('/api/courses', function (data) {
            if (data.length === 0) {
                $('#courses').html('<p>No courses available.</p>');
            } else {
                data.forEach(function (course) {
                    $('#courses').append(`
                        <div class="col">
                            <div class="card h-100">
                                <div class="card-body">
                                    <h5 class="card-title">${course.title}</h5>
                                    <p class="card-text">${course.description}</p>
                                    <button class="btn btn-primary enroll-btn" data-id="${course.id}">Enroll</button>
                                </div>
                            </div>
                        </div>
                    `);
                });
            }
        }).fail(function () {
            $('#courses').html('<p class="text-danger">Failed to load courses.</p>');
        });

        // Handle enroll button click
        $(document).on("click", ".enroll-btn", function () {
            const courseId = $(this).data("id");
            $.ajax({
                url: "/ajax/enroll",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ course_id: courseId }),
                success: function (res) {
                    if (res.success) {
                        alert("Enrolled successfully!");
                        // Update the enrolled courses list if present
                        updateEnrolledCourses();
                    } else {
                        alert(res.message);
                    }
                }
            });
        });
    }

    // Update enrolled courses list in profile (if container exists)
    function updateEnrolledCourses() {
        if ($('#enrolled-courses-list').length) {
            $.get('/api/user/enrollments', function(courses) {
                if (courses.length === 0) {
                    $('#enrolled-courses-list').html('<p>You are not enrolled in any courses yet.</p>');
                } else {
                    let html = '<ul class="list-group">';
                    courses.forEach(function(course) {
                        html += `<li class="list-group-item">
                            <strong>${course.title}</strong> - ${course.description}
                        </li>`;
                    });
                    html += '</ul>';
                    $('#enrolled-courses-list').html(html);
                }
            }).fail(function () {
                $('#enrolled-courses-list').html('<p class="text-danger">Failed to load enrolled courses.</p>');
            });
        }
    }

});

// Cookie helper functions
function setCookie(name, value, days) {
    const d = new Date();
    d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000);
    const expires = "expires=" + d.toUTCString();
    document.cookie = name + "=" + value + ";" + expires + ";path=/";
}

function getCookie(name) {
    const cname = name + "=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const ca = decodedCookie.split(';');
    for (let c of ca) {
        while (c.charAt(0) === ' ') c = c.substring(1);
        if (c.indexOf(cname) === 0) return c.substring(cname.length, c.length);
    }
    return "";
}
