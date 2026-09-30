const userSocket = new WebSocket(
  `${window.location.protocol === "https:" ? "wss" : "ws"}://${window.location.host}/ws/user/`,
);

userSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);

  if (data.action === "wallet_update") {
    const totalEarnings = document.getElementById("total-earnings");
    const pendingBalance = document.getElementById("pending-balance");
    const availableBalance = document.getElementById("available-balance");
    if (totalEarnings && pendingBalance && availableBalance) {
      totalEarnings.innerText = data.wallet.total_earnings;
      pendingBalance.innerText = data.wallet.pending_balance;
      availableBalance.innerText = data.wallet.available_balance;
    }
  }
};

userSocket.onclose = function (e) {
  console.error("تم إغلاق اتصال الـ WebSocket الخاص بالمستخدم");
};

// walletSocket.onmessage = function (e) {
//   const data = JSON.parse(e.data);
//   if (data.action === "wallet_update") {
//     const summary = data.summary;
//     if (document.getElementById("total-balance")) {
//       document.getElementById("total-balance").innerText = summary.total;
//     }
//     if (document.getElementById("frozen-balance")) {
//       document.getElementById("frozen-balance").innerText = summary.frozen;
//     }
//     if (document.getElementById("withdrawable-balance")) {
//       document.getElementById("withdrawable-balance").innerText = summary.withdrawable;
//     }
//   }
// };

// walletSocket.onerror = function (e) {
//   console.error("An error occurred while connecting to the server wallet ! ❌", e);
// };

// const btn = document.getElementById("withdrawBtn");
// const timerText = document.getElementById("timerText");

// let cooldown = 0;
// let interval = null;

// btn.addEventListener("click", function () {
//   if (cooldown > 0) return;

//   fetch("/staff/wallet/withdraw/", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//       "X-CSRFToken": getCookie("csrftoken"),
//     },
//   })
//     .then((res) => res.json())
//     .then((data) => {
//       // 👇 هذا اللي يطبع لك الرد في الكونسل
//       console.log("🔥 Server Response:", data);

//       if (data.success) {
//         startCooldown(300); // 5 دقائق
//       } else {
//         alert("فشل السحب");
//       }
//     })
//     .catch((error) => {
//       console.log("❌ Error:", error);
//     });
// });
// function startCooldown(seconds) {
//   cooldown = seconds;
//   btn.disabled = true;

//   interval = setInterval(() => {
//     cooldown--;

//     let minutes = Math.floor(cooldown / 60);
//     let secs = cooldown % 60;

//     timerText.innerText = `انتظر ${minutes}:${secs.toString().padStart(2, "0")}`;

//     if (cooldown <= 0) {
//       clearInterval(interval);
//       btn.disabled = false;
//       timerText.innerText = "";
//     }
//   }, 1000);
// }

// // // CSRF
// function getCookie(name) {
//   let cookieValue = null;
//   document.cookie.split(";").forEach((cookie) => {
//     cookie = cookie.trim();
//     if (cookie.startsWith(name + "=")) {
//       cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//     }
//   });
//   return cookieValue;
// }
