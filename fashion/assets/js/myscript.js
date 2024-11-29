
// document.addEventListener("DOMContentLoaded", function() {
//     const links = document.querySelectorAll(".option-link");
//     const contents = document.querySelectorAll(".content");

//     links.forEach(link => {
//         link.addEventListener("click", function(event) {
//             event.preventDefault();
//             const targetId = this.getAttribute("data-content-id");

//             // Ẩn tất cả các phần tử nội dung
//             contents.forEach(content => {
//                 content.style.display = "none";
//             });

//             // Hiển thị phần tử nội dung tương ứng
//             const targetContent = document.getElementById(targetId);
//             if (targetContent) {
//                 targetContent.style.display = "block";
//             }

//             // // Đóng offcanvas
//             // const offcanvasElement = document.querySelector('#offcanvasWithBothOptions');
//             // const offcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement);
//             // if (offcanvas) {
//             //     offcanvas.hide();
//             // }
//         });
//     });
// });








document.addEventListener("DOMContentLoaded", function() {
    const subMenus = document.querySelectorAll(".sub-menu"),
        mainButtons = document.querySelectorAll(".sidebar ul > li > button"),
        optionLinks = document.querySelectorAll(".option-link"),
        contents = document.querySelectorAll(".content");

    const onClick = (item) => {
        const isActive = item.classList.contains("active");

        // Ẩn tất cả các sub-menu và loại bỏ lớp active khỏi tất cả các nút
        subMenus.forEach((menu) => (menu.style.height = "0px"));
        mainButtons.forEach((button) => button.classList.remove("active"));
        optionLinks.forEach((link) => link.classList.remove("active"));

        // Nếu nút hiện tại đã active, không cần làm gì thêm
        if (isActive) {
            return;
        }

        // Hiển thị sub-menu tương ứng và thêm lớp active vào nút
        if (item.nextElementSibling && item.nextElementSibling.classList.contains("sub-menu")) {
            const subMenu = item.nextElementSibling,
                ul = subMenu.querySelector("ul");

            subMenu.style.height = `${ul.scrollHeight}px`;
            item.classList.add("active");
        } else {
            item.classList.add("active");
        }

        // Nếu nút có thuộc tính data-content-id, hiển thị nội dung tương ứng
        const targetId = item.getAttribute("data-content-id");
        if (targetId) {
            // Ẩn tất cả các phần tử nội dung
            contents.forEach(content => {
                content.style.display = "none";
            });

            // Hiển thị phần tử nội dung tương ứng
            const targetContent = document.getElementById(targetId);
            if (targetContent) {
                targetContent.style.display = "block";
            }
        }
    };

    // Gắn hàm onClick vào tất cả các nút chính
    mainButtons.forEach(button => {
        button.addEventListener("click", function() {
            onClick(this);
        });
    });

    // Gắn hàm onClick vào tất cả các nút tùy chọn
    optionLinks.forEach(link => {
        link.addEventListener("click", function(event) {
            event.preventDefault();
            onClick(this);
        });
    });
});
  





document.addEventListener('DOMContentLoaded', function() {
    const checkbox = document.getElementById('cbx-51');

    // Kiểm tra giá trị isActive và thiết lập thuộc tính checked của checkbox
    checkbox.checked = isActive; 
});


// const subMenus = document.querySelectorAll(".sub-menu"),
//   buttons = document.querySelectorAll(".sidebar ul button");

// const onClick = (item) => {
//   subMenus.forEach((menu) => (menu.style.height = "0px"));
//   buttons.forEach((button) => button.classList.remove("active"));

//   if (!item.nextElementSibling) {
//     item.classList.add("active");
//     return;
//   }

//   const subMenu = item.nextElementSibling,
//     ul = subMenu.querySelector("ul");

//   if (!subMenu.clientHeight) {
//     subMenu.style.height = `${ul.clientHeight}px`;
//     item.classList.add("active");
    
//   } else {
//     subMenu.style.height = "0px";
//     item.classList.remove("active");
//   }
// };




// Trong tệp myscript.js
function toggleSidebar() {
  const sidebar = document.querySelector('.sidebar');
  sidebar.classList.toggle('active'); // Thêm hoặc xóa class "active"
}



document.addEventListener('DOMContentLoaded', function() {
    // Lấy tất cả các nút "Edit" trong bảng
    const editButtons = document.querySelectorAll('.icon-edit');

    // Lấy nút "Edit" trong modal
    const submitEditButton = document.getElementById('submit-edit-product');

    // Lặp qua từng nút "Edit" trong bảng
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Gán giá trị của nút "Edit" được click vào cho nút "Edit" trong modal
            submitEditButton.value = this.value;
        });
    });
});

