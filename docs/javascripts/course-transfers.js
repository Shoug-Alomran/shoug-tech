(function () {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const adminPage = document.body.dataset.transferPage === "admin";
  let fb,
    db,
    user,
    settings,
    generation = 0,
    receipt = "",
    imageGeneration = 0;
  let unsubscribe = () => {},
    lastOrder = null,
    cursor = null;
  let verification = null;
  let reviewStatus = "pending",
    reviewEmail = "",
    pageStarts = [null],
    pageIndex = 0,
    requestVersion = 0;
  const show = (id, visible) => {
    if ($(id)) $(id).hidden = !visible;
  };
  const message = (text) => {
    $("transfer-message").textContent = text;
  };
  const text = (id, value) => {
    $(id).textContent = value;
  };
  const step = (index) =>
    document.querySelectorAll(".checkout-steps li").forEach((item, i) => {
      if (i === index) item.setAttribute("aria-current", "step");
      else item.removeAttribute("aria-current");
    });
  const errorText = (error) =>
    error.code === "permission-denied"
      ? "This action is not available. Check that you are signed in with the correct verified account. If the problem continues, contact Shoug."
      : "Could not complete the request. Check your connection and try again. Your payment has not been approved automatically.";
  const isCurrent = (version) =>
    version === generation && user && fb.auth().currentUser?.uid === user.uid;

  function reset() {
    requestVersion++;
    verification?.stop();
    verification = null;
    unsubscribe();
    unsubscribe = () => {};
    receipt = "";
    lastOrder = null;
    cursor = null;
    imageGeneration++;
    [
      "transfer-login",
      "transfer-verify",
      "transfer-bank",
      "transfer-form",
      "transfer-admin",
      "transfer-admin-link",
      "transfer-course-link",
    ].forEach((id) => show(id, false));
    step(0);
    if ($("transfer-form")) $("transfer-form").reset();
    if ($("transfer-preview")) {
      $("transfer-preview").removeAttribute("src");
      show("transfer-preview", false);
    }
    if ($("transfer-orders")) $("transfer-orders").replaceChildren();
    if ($("transfer-fields")) $("transfer-fields").disabled = false;
  }

  function ready() {
    return (
      settings?.enabled === true &&
      typeof settings.bankName === "string" &&
      settings.bankName.trim() &&
      typeof settings.beneficiary === "string" &&
      settings.beneficiary.trim() &&
      /^SA\d{22}$/.test(settings.iban) &&
      typeof settings.adminUid === "string" &&
      settings.adminUid.length > 0
    );
  }

  function renderCheckout(order) {
    lastOrder = order;
    step(order?.status === "pending" || order?.status === "approved" ? 2 : 1);
    show("transfer-course-link", order?.status === "approved");
    const canSubmit = ready() && (!order || order.status === "rejected");
    show("transfer-bank", canSubmit);
    show("transfer-form", canSubmit);
    if (order?.status === "pending")
      message(
        "Your receipt is saved and awaiting review. Do not transfer again. Return to this page to check your payment status.",
      );
    else if (order?.status === "approved")
      message(
        "Your bank transfer has been approved. Your course purchase is recorded against this account.",
      );
    else if (order?.status === "rejected")
      message(
        "Your submission needs attention. " +
          (order.reviewNote || "Contact Shoug before transferring again.") +
          (canSubmit ? "\nYou can upload corrected proof below." : ""),
      );
    else
      message(
        ready()
          ? "Signed in as " + user.email + ". Follow the steps below."
          : "Online receipt upload is not open yet. Please wait until receipt submission opens before transferring.",
      );
    if (canSubmit) {
      $("transfer-account-email").value = user.email;
      if (!$("transfer-name").value)
        $("transfer-name").value = order?.fullName || user.displayName || "";
      if (!$("transfer-phone").value)
        $("transfer-phone").value = order?.phone || "";
      text("transfer-email", user.email);
      text("transfer-bank-name", settings.bankName);
      text("transfer-beneficiary", settings.beneficiary);
      text("transfer-iban", settings.iban);
      for (const [id, value] of [
        ["transfer-stc", settings.stcPhone],
        ["transfer-barq", settings.barqPhone],
      ]) {
        const available =
          typeof value === "string" && /^\+9665\d{8}$/.test(value);
        text(id, available ? value : "");
        show(id, available);
        show(id + "-label", available);
      }
      text("transfer-reference", "ETH-" + user.uid);
    }
  }

  async function onAuth(nextUser) {
    const version = ++generation;
    user = nextUser;
    settings = null;
    reset();
    if (!user) {
      show("transfer-login", true);
      message("");
      return;
    }
    if (!user.email) {
      show("transfer-login", true);
      message(
        "This account has no email address. Please sign in using an account with an email.",
      );
      return;
    }
    if (!user.emailVerified) {
      show("transfer-verify", true);
      message("");
      text("verification-email", user.email);
      verification = window.ShougEmailVerification.start({
        user,
        isCurrent: () => isCurrent(version),
        onVerified: (verified) => {
          if (isCurrent(version)) onAuth(verified);
        },
        onStatus: (value) => {
          if (isCurrent(version)) text("verification-status", value);
        },
        onCooldown: (seconds, sending) => {
          if (!isCurrent(version)) return;
          const button = $("transfer-send-verification");
          button.disabled = sending || seconds > 0;
          button.textContent = sending
            ? "Sending…"
            : seconds > 0
              ? "Send a new link in " + seconds + "s"
              : "Send a new link";
        },
      });
      return;
    }
    message("Loading your purchase details…");
    try {
      const config = await db
        .collection("courseCommerce")
        .doc("ethics")
        .get({ source: "server" });
      if (!isCurrent(version)) return;
      settings = config.exists ? config.data() : null;
      if (adminPage) {
        if (settings?.adminUid !== user.uid) {
          message("This page is restricted to the course administrator.");
          return;
        }
        show("transfer-admin", true);
        await loadOrders(true);
      } else {
        show("transfer-admin-link", settings?.adminUid === user.uid);
        unsubscribe = db
          .collection("courseTransfers")
          .doc(user.uid)
          .onSnapshot(
            (snapshot) => {
              if (isCurrent(version))
                renderCheckout(snapshot.exists ? snapshot.data() : null);
            },
            (error) => {
              if (isCurrent(version)) {
                show("transfer-form", false);
                show("transfer-bank", false);
                message(errorText(error));
              }
            },
          );
      }
    } catch (error) {
      if (isCurrent(version))
        message(
          !adminPage && !settings && error.code === "permission-denied"
            ? "Your account is ready. Receipt upload is being set up. Please wait until it opens before transferring. Access requires payment approval."
            : errorText(error),
        );
    }
  }

  // Re-encode the image to remove metadata and keep the private Firestore document
  // below its 1 MiB limit. No public Storage URL or paid upload service is used.
  async function prepareReceipt(file) {
    if (!file || !["image/jpeg", "image/png", "image/webp"].includes(file.type))
      throw new Error("Choose a JPG, PNG or WebP receipt photo.");
    if (file.size > 10 * 1024 * 1024)
      throw new Error("Choose a photo smaller than 10 MB.");
    const image = await createImageBitmap(file).catch(() => {
      throw new Error(
        "This photo could not be read. Try a different JPG or PNG.",
      );
    });
    try {
      const scale = Math.min(1, 1600 / Math.max(image.width, image.height));
      const canvas = document.createElement("canvas");
      canvas.width = Math.max(1, Math.round(image.width * scale));
      canvas.height = Math.max(1, Math.round(image.height * scale));
      const context = canvas.getContext("2d");
      context.fillStyle = "white";
      context.fillRect(0, 0, canvas.width, canvas.height);
      context.drawImage(image, 0, 0, canvas.width, canvas.height);
      for (const quality of [0.88, 0.75, 0.6, 0.45]) {
        const result = canvas.toDataURL("image/jpeg", quality);
        if (result.length <= 700000) return result;
      }
      throw new Error(
        "This image is too detailed to upload. Crop it to the receipt and try again.",
      );
    } finally {
      image.close();
    }
  }

  $("transfer-photo")?.addEventListener("change", async () => {
    const version = generation,
      imageVersion = ++imageGeneration;
    receipt = "";
    show("transfer-preview", false);
    $("transfer-preview").removeAttribute("src");
    try {
      const result = await prepareReceipt($("transfer-photo").files[0]);
      if (!isCurrent(version) || imageVersion !== imageGeneration) return;
      receipt = result;
      $("transfer-preview").src = receipt;
      show("transfer-preview", true);
      message(
        "Check that the receipt preview is readable, then submit it for review.",
      );
    } catch (error) {
      if (isCurrent(version) && imageVersion === imageGeneration) {
        $("transfer-photo").value = "";
        message(error.message);
      }
    }
  });

  $("transfer-form")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (
      !user?.emailVerified ||
      !ready() ||
      !receipt ||
      !$("transfer-consent").checked
    ) {
      message(
        "Sign in with a verified email, choose a receipt photo and confirm the transfer first.",
      );
      return;
    }
    if (!$("transfer-personal-access")?.checked) {
      message(
        "Please agree that course access and materials are for your personal use only.",
      );
      return;
    }
    if (lastOrder && lastOrder.status !== "rejected") return;
    const fullName = $("transfer-name").value.trim();
    let phone = $("transfer-phone").value.replace(/[\s()-]/g, "");
    if (/^05\d{8}$/.test(phone)) phone = "+966" + phone.slice(1);
    if (/^00/.test(phone)) phone = "+" + phone.slice(2);
    if (
      fullName.length < 2 ||
      fullName.length > 120 ||
      !/^\+[1-9]\d{7,14}$/.test(phone)
    ) {
      message(
        "Enter your full name and a valid phone number, including country code for numbers outside Saudi Arabia.",
      );
      return;
    }
    const version = generation,
      buyer = user,
      proof = receipt;
    $("transfer-fields").disabled = true;
    message("Saving your receipt…");
    try {
      await db.runTransaction(async (transaction) => {
        const ref = db.collection("courseTransfers").doc(buyer.uid);
        const existing = await transaction.get(ref);
        if (existing.exists && existing.data().status !== "rejected")
          throw new Error("existing-order");
        transaction.set(ref, {
          uid: buyer.uid,
          email: buyer.email,
          fullName,
          phone,
          course: "ethics",
          amount: 32500,
          currency: "SAR",
          status: "pending",
          receipt: proof,
          submittedAt: fb.firestore.FieldValue.serverTimestamp(),
          reviewedAt: null,
          reviewedBy: "",
          reviewNote: "",
        });
      });
      if (isCurrent(version)) {
        receipt = "";
        $("transfer-form").reset();
        $("transfer-preview").removeAttribute("src");
        show("transfer-preview", false);
        message(
          "Receipt received. Your payment is pending manual review. Do not transfer again.",
        );
      }
    } catch (error) {
      if (isCurrent(version))
        message(
          error.message === "existing-order"
            ? "You already have a submitted purchase. Refresh this page to check its status; do not transfer again."
            : errorText(error),
        );
    } finally {
      if (isCurrent(version)) $("transfer-fields").disabled = false;
    }
  });

  function element(tag, value, className) {
    const node = document.createElement(tag);
    if (value) node.textContent = value;
    if (className) node.className = className;
    return node;
  }

  function orderCard(snapshot) {
    const order = snapshot.data(),
      card = element("details", "", "card admin-row");
    const row = element("summary", "", "review-row");
    const buyer = element("span", "", "review-buyer");
    buyer.append(
      element("strong", order.fullName || "Name not provided"),
      element("span", order.email),
    );
    row.append(
      buyer,
      element(
        "span",
        order.submittedAt?.toDate().toLocaleDateString() || "—",
        "review-date",
      ),
      element("span", "SAR 325", "review-amount"),
      element(
        "span",
        order.status === "pending" ? "Request" : order.status,
        "review-badge " + order.status,
      ),
      element("span", "View ↓", "review-open"),
    );
    card.append(row);
    const statusLine = element("p", "SAR 325 · " + order.status.toUpperCase());
    card.append(
      element("h2", order.fullName || "Name not provided"),
      element("p", "Email: " + order.email),
      element("p", "Phone: " + (order.phone || "Not provided")),
      statusLine,
      element("p", "Reference: ETH-" + order.uid),
      element(
        "p",
        "Submitted: " +
          (order.submittedAt?.toDate().toLocaleString() || "Pending timestamp"),
      ),
    );
    const details = element("details"),
      summary = element("summary", "View transfer proof");
    details.append(summary);
    // Only image data is rendered; user-controlled HTML and external URLs are never used.
    if (
      /^data:image\/jpeg;base64,[A-Za-z0-9+/=]+$/.test(order.receipt || "") &&
      order.receipt.length <= 700000
    ) {
      const photo = element("img", "", "receipt");
      photo.alt = "Transfer proof from " + order.email;
      photo.src = order.receipt;
      details.append(photo);
    } else
      details.append(
        element(
          "p",
          "Receipt could not be displayed. Do not approve without checking the payment.",
        ),
      );
    card.append(details);
    if (order.reviewNote)
      card.append(element("p", "Review note: " + order.reviewNote));
    if (order.status !== "pending") return card;
    const label = element("label", "Review note (required when rejecting)"),
      note = element("textarea");
    note.id = "review-" + snapshot.id;
    note.maxLength = 500;
    label.htmlFor = note.id;
    card.append(label, note);
    const checkLabel = element("label"),
      check = element("input");
    check.type = "checkbox";
    checkLabel.append(
      check,
      document.createTextNode(
        " I verified that SAR 325 arrived in my bank account.",
      ),
    );
    card.append(checkLabel);
    const actions = element("div", "", "actions"),
      approve = element("button", "Approve payment"),
      reject = element("button", "Reject / request correction");
    approve.type = reject.type = "button";
    approve.disabled = true;
    check.addEventListener("change", () => {
      approve.disabled = !check.checked;
    });
    actions.append(approve, reject);
    card.append(actions);
    async function review(status) {
      if (status === "approved" && !check.checked) return;
      if (status === "rejected" && !note.value.trim()) {
        note.focus();
        message("Add a note explaining what the buyer should correct.");
        return;
      }
      const version = generation,
        reviewer = user?.uid;
      if (!reviewer || settings?.adminUid !== reviewer) return;
      approve.disabled = reject.disabled = check.disabled = true;
      try {
        await db.runTransaction(async (transaction) => {
          const current = await transaction.get(snapshot.ref);
          if (!current.exists || current.data().status !== "pending")
            throw new Error("already-reviewed");
          transaction.update(snapshot.ref, {
            status,
            reviewedAt: fb.firestore.FieldValue.serverTimestamp(),
            reviewedBy: reviewer,
            reviewNote: note.value.trim(),
          });
        });
        if (isCurrent(version)) {
          message("Payment " + status + " for " + order.email + ".");
          statusLine.textContent = "SAR 325 · " + status.toUpperCase();
          actions.remove();
          checkLabel.remove();
          note.disabled = true;
          loadOrders(true);
        }
      } catch (error) {
        if (isCurrent(version)) {
          message(
            error.message === "already-reviewed"
              ? "This transfer was already reviewed. Refresh to see its current status."
              : errorText(error),
          );
          approve.disabled = !check.checked;
          reject.disabled = check.disabled = false;
        }
      }
    }
    approve.addEventListener("click", () => review("approved"));
    reject.addEventListener("click", () => review("rejected"));
    return card;
  }

  async function loadOrders(first) {
    const version = generation,
      request = ++requestVersion;
    if (settings?.adminUid !== user?.uid) return;
    if (first) {
      pageIndex = 0;
      pageStarts = [null];
      cursor = null;
    }
    $("transfer-reload").disabled = $("transfer-more").disabled = true;
    message(
      "Loading " +
        (reviewStatus === "all"
          ? "all payments"
          : reviewStatus === "pending"
            ? "requests"
            : reviewStatus + " payments") +
        "…",
    );
    $("transfer-orders").setAttribute("aria-busy", "true");
    try {
      let query = db.collection("courseTransfers").limit(10);
      if (reviewStatus !== "all")
        query = query.where("status", "==", reviewStatus);
      if (reviewEmail) query = query.where("email", "==", reviewEmail);
      if (pageStarts[pageIndex])
        query = query.startAfter(pageStarts[pageIndex]);
      const result = await query.get({ source: "server" });
      if (!isCurrent(version) || request !== requestVersion) return;
      $("transfer-orders").replaceChildren(...result.docs.map(orderCard));
      cursor = result.docs[result.docs.length - 1] || null;
      show("transfer-more", result.size === 10);
      if ($("transfer-prev")) $("transfer-prev").disabled = pageIndex === 0;
      if ($("review-page"))
        $("review-page").textContent = "Page " + (pageIndex + 1);
      message(
        result.empty
          ? "No " +
              (reviewStatus === "all"
                ? "payments"
                : reviewStatus === "pending"
                  ? "requests"
                  : reviewStatus + " payments") +
              (reviewEmail ? " for this email." : " to show.")
          : "Showing " +
              result.size +
              " " +
              (reviewStatus === "all"
                ? "payments"
                : reviewStatus === "pending"
                  ? "requests"
                  : reviewStatus + " payments") +
              " on this page.",
      );
    } catch (error) {
      if (isCurrent(version) && request === requestVersion)
        message(errorText(error));
    } finally {
      if (isCurrent(version) && request === requestVersion) {
        $("transfer-reload").disabled = $("transfer-more").disabled = false;
        $("transfer-orders").setAttribute("aria-busy", "false");
      }
    }
  }

  $("transfer-signin").addEventListener("click", () => {
    if (window.__shougOpenAuthModal) window.__shougOpenAuthModal();
    else message("Sign-in is still loading. Please try again shortly.");
  });
  $("transfer-send-verification").addEventListener("click", () =>
    verification?.resend(),
  );
  $("transfer-reload")?.addEventListener("click", () => loadOrders(true));
  $("transfer-more")?.addEventListener("click", () => {
    if (!cursor) return;
    pageStarts[++pageIndex] = cursor;
    loadOrders(false);
  });
  $("transfer-prev")?.addEventListener("click", () => {
    if (pageIndex > 0) {
      pageIndex--;
      loadOrders(false);
    }
  });
  document.querySelectorAll("[data-status]").forEach((button) =>
    button.addEventListener("click", () => {
      reviewStatus = button.dataset.status;
      document
        .querySelectorAll("[data-status]")
        .forEach((tab) =>
          tab.setAttribute("aria-pressed", String(tab === button)),
        );
      $("transfer-orders").replaceChildren();
      loadOrders(true);
    }),
  );
  $("review-search")?.addEventListener("submit", (event) => {
    event.preventDefault();
    reviewEmail = $("review-email").value.trim();
    loadOrders(true);
  });
  $("review-clear")?.addEventListener("click", () => {
    $("review-email").value = "";
    reviewEmail = "";
    loadOrders(true);
  });
  function boot() {
    if (fb) return;
    fb = window.__shoug_fb;
    db = fb.firestore();
    fb.auth().onAuthStateChanged(onAuth);
  }
  if (window.__shoug_fb) boot();
  else window.addEventListener("shoug:fb", boot, { once: true });
  setTimeout(() => {
    if (!fb)
      message(
        "Sign-in could not load. Check your connection or browser content blocker and reload this page.",
      );
  }, 15000);
})();
