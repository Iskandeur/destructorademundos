import sys
import dns.resolver
import smtplib

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r') as f:
    emails = [e.strip() for e in f.readlines()]

results = []
total = len(emails)
for i, email in enumerate(emails, start=1):
    print(str(i) + '/' + str(total) + ' ' + email)
    try:
        domain = email.split('@')[1]
        records = dns.resolver.resolve(domain, 'MX')
        mx = str(sorted(records, key=lambda r: r.preference)[0].exchange)
        s = smtplib.SMTP()
        s.connect(mx)
        s.helo(s.local_hostname)
        s.mail('test@example.com')
        code, _ = s.rcpt(email)
        s.quit()
        if code == 250:
            results.append(email + ' valid')
        else:
            results.append(email + ' invalid')
    except:
        results.append(email + ' invalid')

with open(output_file, 'w') as f:
    for r in results:
        f.write(r + '\n')
        print(r)
