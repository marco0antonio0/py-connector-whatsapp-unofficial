from services import automation

# ======================================================
#        this is the guide for use the code
# ======================================================

# create instance
instance = automation(gui=False)

# start process
instance.start()

# loop the checking if having the new messages
while True:
    # check if new message exists
    newIdUser = instance.VerificarNovaMensagem()
    # if case exist
    if newIdUser:
        # so aplly an return last message of the contact
        lastMessage = instance.pegar_ultima_mensagem()
        # show last messagen
        print(lastMessage)

    # this is necessary for got back the homescreen page
    instance.go_to_home()
