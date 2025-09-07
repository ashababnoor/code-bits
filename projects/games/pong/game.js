const canvas = document.getElementById('pong');
const ctx = canvas.getContext('2d');

// Game constants
const PADDLE_WIDTH = 10, PADDLE_HEIGHT = 100;
const BALL_SIZE = 14;
const PLAYER_X = 20;
const AI_X = canvas.width - PLAYER_X - PADDLE_WIDTH;
const PADDLE_SPEED = 7;
const AI_SPEED = 4;

// Game objects
let player = {
  x: PLAYER_X,
  y: canvas.height / 2 - PADDLE_HEIGHT / 2,
  width: PADDLE_WIDTH,
  height: PADDLE_HEIGHT,
};

let ai = {
  x: AI_X,
  y: canvas.height / 2 - PADDLE_HEIGHT / 2,
  width: PADDLE_WIDTH,
  height: PADDLE_HEIGHT,
};

let ball = {
  x: canvas.width / 2 - BALL_SIZE / 2,
  y: canvas.height / 2 - BALL_SIZE / 2,
  size: BALL_SIZE,
  speedX: 5 * (Math.random() < 0.5 ? 1 : -1),
  speedY: (Math.random() * 4 + 2) * (Math.random() < 0.5 ? 1 : -1),
};

function drawRect(x, y, w, h, color = "#fff") {
  ctx.fillStyle = color;
  ctx.fillRect(x, y, w, h);
}

function drawBall(x, y, size, color = "#fff") {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(x + size / 2, y + size / 2, size / 2, 0, Math.PI * 2);
  ctx.fill();
}

function resetBall() {
  ball.x = canvas.width / 2 - BALL_SIZE / 2;
  ball.y = canvas.height / 2 - BALL_SIZE / 2;
  ball.speedX = 5 * (Math.random() < 0.5 ? 1 : -1);
  ball.speedY = (Math.random() * 4 + 2) * (Math.random() < 0.5 ? 1 : -1);
}

function draw() {
  // Clear
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Middle dashed line
  ctx.setLineDash([10, 10]);
  ctx.strokeStyle = "#888";
  ctx.beginPath();
  ctx.moveTo(canvas.width/2, 0);
  ctx.lineTo(canvas.width/2, canvas.height);
  ctx.stroke();
  ctx.setLineDash([]);

  // Paddles and ball
  drawRect(player.x, player.y, player.width, player.height);
  drawRect(ai.x, ai.y, ai.width, ai.height);
  drawBall(ball.x, ball.y, ball.size);
}

function clamp(val, min, max) {
  return Math.max(min, Math.min(max, val));
}

function update() {
  // Ball movement
  ball.x += ball.speedX;
  ball.y += ball.speedY;

  // Wall collision (top/bottom)
  if (ball.y < 0) {
    ball.y = 0;
    ball.speedY = -ball.speedY;
  }
  if (ball.y + ball.size > canvas.height) {
    ball.y = canvas.height - ball.size;
    ball.speedY = -ball.speedY;
  }

  // Paddle collision
  // Player paddle
  if (
    ball.x < player.x + player.width &&
    ball.x + ball.size > player.x &&
    ball.y < player.y + player.height &&
    ball.y + ball.size > player.y
  ) {
    ball.x = player.x + player.width;
    ball.speedX = -ball.speedX;
    // Add a bit of "english"
    let deltaY = ball.y + ball.size / 2 - (player.y + player.height / 2);
    ball.speedY += deltaY * 0.15;
  }

  // AI paddle
  if (
    ball.x + ball.size > ai.x &&
    ball.x < ai.x + ai.width &&
    ball.y < ai.y + ai.height &&
    ball.y + ball.size > ai.y
  ) {
    ball.x = ai.x - ball.size;
    ball.speedX = -ball.speedX;
    let deltaY = ball.y + ball.size / 2 - (ai.y + ai.height / 2);
    ball.speedY += deltaY * 0.15;
  }

  // Score detection (ball out of bounds)
  if (ball.x < 0 || ball.x + ball.size > canvas.width) {
    resetBall();
  }

  // AI movement: follow the ball.y, but not perfectly
  let aiCenter = ai.y + ai.height / 2;
  let ballCenter = ball.y + ball.size / 2;
  if (aiCenter < ballCenter - 10) {
    ai.y += AI_SPEED;
  } else if (aiCenter > ballCenter + 10) {
    ai.y -= AI_SPEED;
  }
  ai.y = clamp(ai.y, 0, canvas.height - ai.height);
}

function gameLoop() {
  update();
  draw();
  requestAnimationFrame(gameLoop);
}

// Mouse movement controls left paddle
canvas.addEventListener('mousemove', function(e) {
  let rect = canvas.getBoundingClientRect();
  let mouseY = e.clientY - rect.top;
  player.y = clamp(mouseY - player.height / 2, 0, canvas.height - player.height);
});

// Start game
gameLoop();
