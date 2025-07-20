# Dockerfile to test script-installer.sh
FROM ubuntu:24.04

# Install bash and other essentials
RUN apt-get update && apt-get install -y bash

# Create a test user
RUN useradd -ms /bin/bash tester
USER tester
WORKDIR /home/tester

# Copy script-installer.sh and a sample script
COPY script-installer.sh /home/tester/script-installer.sh
COPY test-script.sh /home/tester/test-script.sh

# Make both scripts executable
RUN chmod +x /home/tester/script-installer.sh /home/tester/test-script.sh

# Set up PATH for ~/bin
RUN mkdir -p /home/tester/bin && echo 'export PATH="$HOME/bin:$PATH"' >> /home/tester/.bashrc

# Entrypoint for testing
CMD ["/bin/bash"]
